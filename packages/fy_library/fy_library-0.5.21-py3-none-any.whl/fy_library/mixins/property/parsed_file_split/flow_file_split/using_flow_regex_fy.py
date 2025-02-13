# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
property flow_file_split: FlowFileSplitModel using flow_regex:
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
from fy_library.mixins.property.parsed_file_split.flow_file_split.abc_fy import (
    FlowFileSplit_PropertyMixin_ABC,
    FlowFileSplitModel,
)

_FLOW_STRING_SPLIT_REGEX: Final = re.compile(
    rf"flow\s+(?P<flow_name>{FY_ENTITY_REGEX_STRING})\s*"
    rf"(?:\[(?P<generics_def>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?\s*"
    rf"(?:\((?P<declared_base_flow>{FY_ENTITY_REGEX_STRING})(?:\[(?P<declared_base_flow_generics_def>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?\))?"
    rf"(?:\s+->\s+(?P<return_type>{PYTHON_MULTI_ENTITY_REGEX_STRING}))?:\s*\n"
)


# fy:start ===>>>
class FlowFileSplit_UsingFlowRegex_PropertyMixin(
    # Property Mixins
    FlowFileSplit_PropertyMixin_ABC,
    FyCode_PropertyMixin_ABC,
    FyPyFileToParse_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _flow_file_split(self) -> FlowFileSplitModel:
        # fy:end <<<===
        flow_file_split = _FLOW_STRING_SPLIT_REGEX.split(self._fy_code)

        assert (
            (len(flow_file_split)) == 7
        ), f"Flow file split length {len(flow_file_split)} is invalid in {self._fy_py_file_to_parse}"

        flow_file_split_model = FlowFileSplitModel(
            user_imports=flow_file_split[0],
            flow_name=flow_file_split[1],
            generics_def=flow_file_split[2] or "",
            declared_base_flow=flow_file_split[3] or "",
            declared_base_flow_generics_def=flow_file_split[4] or "",
            return_type=flow_file_split[5] or "",
            mixins=flow_file_split[6],
        )

        return flow_file_split_model
