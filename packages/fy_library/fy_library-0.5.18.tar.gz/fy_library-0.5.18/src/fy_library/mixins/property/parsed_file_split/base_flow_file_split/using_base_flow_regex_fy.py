# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from fy_library.mixins.property.parsed_file_split.base_flow_file_split.abc_fy import BaseFlowFileSplitModel


property base_flow_file_split: BaseFlowFileSplitModel using base_flow_regex:
    property fy_py_file_to_parse
    property fy_code
fy"""

import abc
import re
from functools import cached_property
from typing import Final, List

from fy_library.constants import (
    FY_ENTITY_REGEX_STRING,
    PYTHON_MULTI_ENTITY_REGEX_STRING,
)
from fy_library.domain.annotation_object import Annotation, AnnotationKind
from fy_library.mixins.property.fy_file.fy_code.abc_fy import FyCode_PropertyMixin_ABC
from fy_library.mixins.property.fy_py_file.fy_py_file_to_parse.abc_fy import (
    FyPyFileToParse_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsed_file_split.base_flow_file_split.abc_fy import (
    BaseFlowFileSplit_PropertyMixin_ABC,
    BaseFlowFileSplitModel,
)

_BASE_FLOW_STRING_SPLIT_REGEX: Final = re.compile(
    rf"base\s+flow\s+(?P<flow_name>{FY_ENTITY_REGEX_STRING})\s*"
    rf"(?:\[(?P<generics_def>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?\s*"
    rf"(?:\((?P<declared_base_flow>{FY_ENTITY_REGEX_STRING})(?:\[(?P<declared_base_flow_generics_def>{PYTHON_MULTI_ENTITY_REGEX_STRING})])?\))?"
    rf"(?:\s+->\s+(?P<return_type>{PYTHON_MULTI_ENTITY_REGEX_STRING}))?:\s*\n"
)

_CHECK_ANNOTATIONS: Final = re.compile(r"(?P<annotations>@\w+)")


# fy:start ===>>>
class BaseFlowFileSplit_UsingBaseFlowRegex_PropertyMixin(
    # Property Mixins
    BaseFlowFileSplit_PropertyMixin_ABC,
    FyCode_PropertyMixin_ABC,
    FyPyFileToParse_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _base_flow_file_split(self) -> BaseFlowFileSplitModel:
        # fy:end <<<===
        base_flow_file_split = _BASE_FLOW_STRING_SPLIT_REGEX.split(self._fy_code)

        check_if_annotations_are_ordered = [
            bool(re.match(_CHECK_ANNOTATIONS, maybe_annotation))
            for maybe_annotation in base_flow_file_split[0].split("\n")
            if maybe_annotation != ""
        ]

        first_annotation_found: bool = False
        for is_annotation in check_if_annotations_are_ordered:
            if is_annotation and not first_annotation_found:
                first_annotation_found = True
            if not is_annotation and first_annotation_found:
                raise AssertionError(
                    f"Base flow {base_flow_file_split[1]} has unordered annotations."
                )

        annotations: List[Annotation] = []

        all_annotations = re.findall(_CHECK_ANNOTATIONS, base_flow_file_split[0])
        for annotation in all_annotations:
            annotation_object = Annotation(
                kind=AnnotationKind(annotation),
            )
            annotations.append(annotation_object)

        user_imports = re.sub(_CHECK_ANNOTATIONS, "", base_flow_file_split[0])

        assert (
            (len(base_flow_file_split)) == 7
        ), f"Flow file split length {len(base_flow_file_split)} is invalid in {self._fy_py_file_to_parse}"

        base_flow_file_split_model = BaseFlowFileSplitModel(
            user_imports=user_imports,
            annotations=annotations,
            base_flow_name=base_flow_file_split[1],
            generics_def=base_flow_file_split[2] or "",
            declared_base_flow=base_flow_file_split[3] or "",
            declared_base_flow_generics_def=base_flow_file_split[4] or "",
            return_type=base_flow_file_split[5],
            mixins=base_flow_file_split[6],
        )

        return base_flow_file_split_model
