# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import inspect
from typing import get_origin, Type, Any


def is_parameter_subclass_type(
    parameter: inspect.Parameter, class_type: Type[Any]
) -> bool:
    parameter_origin = get_origin(parameter.annotation)
    return (
        parameter_origin is not None
        and issubclass(parameter_origin, class_type)
        or parameter_origin is None
        and issubclass(parameter.annotation, class_type)
        or isinstance(parameter.default, class_type)
    )
