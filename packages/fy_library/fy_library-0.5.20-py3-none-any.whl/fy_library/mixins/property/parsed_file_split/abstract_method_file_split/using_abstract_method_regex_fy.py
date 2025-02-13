# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from fy_library.mixins.property.parsed_file_split.abstract_method_file_split.abc_fy import AbstractMethodFileSplitModel


property abstract_method_file_split: AbstractMethodFileSplitModel using abstract_method_regex:
    property fy_py_file_to_parse
    property fy_code
fy"""

import abc
import re
from functools import cached_property
from typing import Final

from fy_library.constants import (
    FY_ENTITY_REGEX_STRING,
    PYTHON_ARGUMENTS_REGEX_STRING,
    PYTHON_MULTI_ENTITY_REGEX_STRING,
)
from fy_library.mixins.property.fy_file.fy_code.abc_fy import FyCode_PropertyMixin_ABC
from fy_library.mixins.property.fy_py_file.fy_py_file_to_parse.abc_fy import (
    FyPyFileToParse_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsed_file_split.abstract_method_file_split.abc_fy import (
    AbstractMethodFileSplit_PropertyMixin_ABC,
    AbstractMethodFileSplitModel,
)

_ABSTRACT_METHOD_REGEX: Final = re.compile(
    rf"method\s+(?P<abstract_method_name>{FY_ENTITY_REGEX_STRING})"
    rf"\s*(?:\[(?P<generics>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?"
    rf"\s*(?:\((?P<arguments>{PYTHON_ARGUMENTS_REGEX_STRING})\))?"
    rf"\s*(?:->\s*(?P<return_type>{PYTHON_MULTI_ENTITY_REGEX_STRING}))?\s*$",
)


# fy:start ===>>>
class AbstractMethodFileSplit_UsingAbstractMethodRegex_PropertyMixin(
    # Property Mixins
    AbstractMethodFileSplit_PropertyMixin_ABC,
    FyCode_PropertyMixin_ABC,
    FyPyFileToParse_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _abstract_method_file_split(self) -> AbstractMethodFileSplitModel:
        # fy:end <<<===
        abstract_method_file_split = _ABSTRACT_METHOD_REGEX.split(self._fy_code)

        assert (
            len(abstract_method_file_split) == 6
        ), f"Abstract Method file split length {len(abstract_method_file_split)} is invalid in {self._fy_py_file_to_parse}."

        assert (
            abstract_method_file_split[4] is not None
        ), f"Abstract method requires return type in {self._fy_py_file_to_parse}."

        abstract_method_file_split_model = AbstractMethodFileSplitModel(
            user_imports=abstract_method_file_split[0],
            abstract_method_name=abstract_method_file_split[1],
            generics_def=abstract_method_file_split[2] or "",
            arguments=abstract_method_file_split[3],
            return_type=abstract_method_file_split[4] or "",
        )

        return abstract_method_file_split_model
