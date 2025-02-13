# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from fy_library.mixins.property.parsed_file_split.abstract_property_file_split.abc_fy import AbstractPropertyFileSplitModel


property abstract_property_file_split: AbstractPropertyFileSplitModel using abstract_property_regex:
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
)
from fy_library.mixins.property.fy_file.fy_code.abc_fy import FyCode_PropertyMixin_ABC
from fy_library.mixins.property.fy_py_file.fy_py_file_to_parse.abc_fy import (
    FyPyFileToParse_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsed_file_split.abstract_property_file_split.abc_fy import (
    AbstractPropertyFileSplit_PropertyMixin_ABC,
    AbstractPropertyFileSplitModel,
)

_ABSTRACT_PROPERTY_REGEX: Final = re.compile(
    rf"property\s+(?P<abstract_property_name>{FY_ENTITY_REGEX_STRING})"
    rf"(?:\[(?P<generic_type>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?"
    rf":\s*(?P<return_type>{PYTHON_MULTI_ENTITY_REGEX_STRING})\s*$",
    flags=re.DOTALL,
)


# fy:start ===>>>
class AbstractPropertyFileSplit_UsingAbstractPropertyRegex_PropertyMixin(
    # Property Mixins
    AbstractPropertyFileSplit_PropertyMixin_ABC,
    FyCode_PropertyMixin_ABC,
    FyPyFileToParse_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _abstract_property_file_split(self) -> AbstractPropertyFileSplitModel:
        # fy:end <<<===
        abstract_property_file_split = _ABSTRACT_PROPERTY_REGEX.split(self._fy_code)

        assert (
            len(abstract_property_file_split) == 5
        ), f"Abstract property file split length {len(abstract_property_file_split)} in {self._fy_py_file_to_parse}"

        assert (
            abstract_property_file_split[3] is not None
        ), f"Abstract property requires property type in {self._fy_py_file_to_parse}"

        abstract_property_file_split_model = AbstractPropertyFileSplitModel(
            user_imports=abstract_property_file_split[0],
            abstract_property_name=abstract_property_file_split[1],
            generics_def=abstract_property_file_split[2] or "",
            property_type=abstract_property_file_split[3],
        )

        return abstract_property_file_split_model
