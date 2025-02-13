# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import abc
from typing import List

from pydantic import BaseModel

from fy_library.domain.mixin_models import (
    MethodMixinModel,
    AbstractMethodModel,
    AbstractPropertyModel,
    PropertyMixinModel,
)
from fy_library.domain.parsed_fy_py_file import ParsedAbstractPropertyFyPyFile
from fy_library.domain.parsed_fy_py_file_kind import ParsedFyPyFileKind
from fy_library.domain.python_entity_name import PythonEntityName


class BaseTemplateModel(BaseModel, abc.ABC):
    python_class_name: PythonEntityName


class TemporaryBaseTemplateModel(BaseTemplateModel):
    entity_key_value: tuple[ParsedFyPyFileKind, str]


class MethodTemplateModel(BaseTemplateModel):
    method_name: PythonEntityName
    abstract_property_non_generic_mixins: List[AbstractPropertyModel]
    abstract_property_generic_mixins: List[AbstractPropertyModel]
    abstract_method_non_generic_mixins: List[AbstractMethodModel]
    abstract_method_generic_mixins: List[AbstractMethodModel]
    generics_def: str
    arguments: str | None
    implementation_name: PythonEntityName
    return_type: str


class AbstractMethodTemplateModel(BaseTemplateModel):
    abstract_method_name: PythonEntityName
    generics_def: str
    arguments: str | None
    return_type: str


class AbstractPropertyTemplateModel(BaseTemplateModel):
    abstract_property_name: PythonEntityName
    generics_def: str
    property_type: str


class FlowTemplateModel(BaseTemplateModel):
    flow_name: PythonEntityName
    generics_def: str
    declared_base_flow: PythonEntityName | None
    declared_base_flow_generics_def: str
    return_type: str
    properties: list[PropertyMixinModel]
    properties_without_setters: list[PropertyMixinModel]
    methods: list[MethodMixinModel]
    property_setters: list[ParsedAbstractPropertyFyPyFile]
    property_constant_setters: list[PropertyMixinModel]
    property_mixins_in_use: list[PropertyMixinModel]
    method_mixins_in_use: list[MethodMixinModel]


class BaseFlowTemplateModel(BaseTemplateModel):
    base_flow_name: PythonEntityName
    generics_def: str
    declared_base_flow_python_class_name: PythonEntityName | None
    declared_base_flow_generics_def: str
    return_type: str
    properties: List[PropertyMixinModel]
    methods: List[MethodMixinModel]
    abstract_property_mixins: List[AbstractPropertyModel]
    abstract_method_mixins: List[AbstractMethodModel]
    property_setters: List[ParsedAbstractPropertyFyPyFile]
    callable_annotation: bool


class PropertyTemplateModel(BaseTemplateModel):
    property_name: PythonEntityName
    implementation_name: PythonEntityName
    abstract_property_mixins: List[AbstractPropertyModel]
    generics_def: str
    property_type: str


class PropertySetterTemplateModel(BaseTemplateModel):
    property_name: PythonEntityName
    property_type: str
    generics_def: str
