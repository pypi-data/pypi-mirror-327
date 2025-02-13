# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
property method_file_split: MethodFileSplitModel using method_regex:
    property fy_py_file_to_parse
    property fy_code
fy"""

import abc
import re
from functools import cached_property
from typing import Final


from fy_library.constants import (
    FY_ENTITY_REGEX_STRING,
    PYTHON_MULTI_ENTITY_REGEX_STRING,
    PYTHON_ARGUMENTS_REGEX_STRING,
)
from fy_library.mixins.property.fy_file.fy_code.abc_fy import FyCode_PropertyMixin_ABC
from fy_library.mixins.property.fy_py_file.fy_py_file_to_parse.abc_fy import (
    FyPyFileToParse_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsed_file_split.method_file_split.abc_fy import (
    MethodFileSplit_PropertyMixin_ABC,
    MethodFileSplitModel,
)

_METHOD_STRING_SPLIT_REGEX: Final = re.compile(
    rf"method\s+(?P<method_name>{FY_ENTITY_REGEX_STRING})\s*"
    rf"(?:\[(?P<generics_def>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?"
    rf"(?:\((?P<arguments>{PYTHON_ARGUMENTS_REGEX_STRING})\))?\s+->"
    rf"\s+(?P<return_type>{PYTHON_MULTI_ENTITY_REGEX_STRING})\s+"
    rf"using\s+(?P<implementation_name>{FY_ENTITY_REGEX_STRING})\s*:\s*\n"
)


# fy:start ===>>>
class MethodFileSplit_UsingMethodRegex_PropertyMixin(
    # Property Mixins
    FyCode_PropertyMixin_ABC,
    FyPyFileToParse_PropertyMixin_ABC,
    MethodFileSplit_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _method_file_split(self) -> MethodFileSplitModel:
        # fy:end <<<===
        method_file_split = _METHOD_STRING_SPLIT_REGEX.split(self._fy_code)

        assert (
            (len(method_file_split)) == 7
        ), f"Method file split length {len(method_file_split)} is invalid in {self._fy_py_file_to_parse}"

        method_file_split_model = MethodFileSplitModel(
            user_imports=method_file_split[0],
            method_name=method_file_split[1],
            generics_def=method_file_split[2] or "",
            arguments=method_file_split[3],
            implementation_name=method_file_split[5],
            return_type=method_file_split[4],
            mixins=method_file_split[6],
        )

        return method_file_split_model
