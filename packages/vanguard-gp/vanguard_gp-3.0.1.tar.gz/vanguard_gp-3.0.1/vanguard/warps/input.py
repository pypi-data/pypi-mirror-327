# © Crown Copyright GCHQ
#
# Licensed under the GNU General Public License, version 3 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains the Python decorators for applying input warping.
"""

from typing import Any, TypeVar

import torch
from typing_extensions import Self

from vanguard import utils
from vanguard.base import GPController
from vanguard.decoratorutils import Decorator, process_args, wraps_class
from vanguard.warps.basefunction import WarpFunction

ControllerT = TypeVar("ControllerT", bound=GPController)
ModuleT = TypeVar("ModuleT", bound=torch.nn.Module)


class _SetModuleInputWarp:
    """
    Set the input warp for a `torch.nn.Module` instance.

    Input warping is formulated so that the index (input) space of the GP must be transformed using the input warp.
    As such, to obtain the desired model with the chosen mean and kernel in the warped space, the mean and kernel
    functions must be composed with the inverse warp.

    Since kernels and means are implemented as subclasses of `torch.nn.Module` in GPyTorch, we can apply the inverse
    warping to both using this class alone.
    """

    def __init__(self, warp: WarpFunction) -> None:
        self.warp = warp

    def __call__(self, module_class: type[ModuleT]) -> type[ModuleT]:
        warp = self.warp

        @wraps_class(module_class)
        class InnerClass(module_class):
            """Apply the inner warp."""

            def forward(self, *args: Any, **kwargs: Any):
                """Map all inputs through the warp inverse."""
                inverse_warped_inputs = [warp.inverse(x) for x in args]
                return super().forward(*inverse_warped_inputs, **kwargs)

        return InnerClass


class SetInputWarp(Decorator):
    """
    Apply input warping to a GP to achieve non-Gaussian input uncertainty.

    :Example:
            >>> from vanguard.base import GPController
            >>> from vanguard.warps.warpfunctions import BoxCoxWarpFunction
            >>>
            >>> @SetInputWarp(BoxCoxWarpFunction(1))
            ... class MyController(GPController):
            ...     pass
    """

    def __init__(self, warp_function: WarpFunction, **kwargs: Any) -> None:
        """
        Initialise self.

        :param warp_function: The warp function to be applied to the GP inputs.
        :param kwargs: Keyword arguments passed to :class:`~vanguard.decoratorutils.basedecorator.Decorator`.
        """
        super().__init__(framework_class=GPController, required_decorators={}, **kwargs)
        self.warp_function = warp_function

    def _decorate_class(self, cls: type[ControllerT]) -> type[ControllerT]:
        warp_function = self.warp_function

        @wraps_class(cls)
        class InnerClass(cls):
            """
            A wrapper for applying a warp to inputs for non-Gaussian input uncertainty.
            """

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                all_parameters_as_kwargs = process_args(super().__init__, *args, **kwargs)
                self.rng = utils.optional_random_generator(all_parameters_as_kwargs.pop("rng", None))

                module_decorator = _SetModuleInputWarp(warp_function)
                mean_class = all_parameters_as_kwargs.pop("mean_class")
                kernel_class = all_parameters_as_kwargs.pop("kernel_class")
                super().__init__(
                    kernel_class=module_decorator(kernel_class),
                    mean_class=module_decorator(mean_class),
                    rng=self.rng,
                    **all_parameters_as_kwargs,
                )
                self.input_warp = warp_function

            @classmethod
            def new(cls, instance: Self, **kwargs: Any) -> Self:
                """Also apply warping to the new instance."""
                new_instance = super().new(instance, **kwargs)
                new_instance.input_warp = instance.input_warp
                return new_instance

        return InnerClass
