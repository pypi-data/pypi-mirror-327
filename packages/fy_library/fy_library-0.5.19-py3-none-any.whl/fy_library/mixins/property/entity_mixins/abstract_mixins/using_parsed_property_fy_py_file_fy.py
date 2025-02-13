# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from typing import List
from fy_library.domain.mixin_models import BaseMixinModel


property abstract_mixins: List[BaseMixinModel] using parsed_property_fy_py_file:
    property parsed_fy_py_file
fy"""

import abc
from functools import cached_property
from typing import List, cast

from fy_library.domain.mixin_models import BaseMixinModel
from fy_library.domain.parsed_fy_py_file import (
    ParsedPropertyFyPyFile,
)
from fy_library.mixins.property.entity_mixins.abstract_mixins.abc_fy import (
    AbstractMixins_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsed_fy_py.parsed_fy_py_file.abc_fy import (
    ParsedFyPyFile_PropertyMixin_ABC,
)


# fy:start ===>>>
class AbstractMixins_UsingParsedPropertyFyPyFile_PropertyMixin(
    # Property Mixins
    AbstractMixins_PropertyMixin_ABC,
    ParsedFyPyFile_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _abstract_mixins(self) -> List[BaseMixinModel]:
        # fy:end <<<===
        parsed_property_fy_py_file = self._parsed_fy_py_file
        assert isinstance(parsed_property_fy_py_file, ParsedPropertyFyPyFile)

        return cast(
            List[BaseMixinModel], parsed_property_fy_py_file.abstract_property_mixins
        )
