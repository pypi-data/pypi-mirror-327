# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from typing import List


property import_any: List[str] using property_setters_exists:
    property property_setter_mixins
    property property_constant_setter_mixins
fy"""

import abc
from functools import cached_property
from typing import List

from fy_library.mixins.property.property_setters.property_constant_setter_mixins.abc_fy import (
    PropertyConstantSetterMixins_PropertyMixin_ABC,
)
from fy_library.mixins.property.property_setters.property_setter_mixins.abc_fy import (
    PropertySetterMixins_PropertyMixin_ABC,
)


# fy:start ===>>>
class ImportAny_UsingPropertySettersExists_PropertyMixin(
    # Property Mixins
    PropertyConstantSetterMixins_PropertyMixin_ABC,
    PropertySetterMixins_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _import_any(self) -> List[str]:
        # fy:end <<<===
        return (
            ["from typing import Any"]
            if self._property_setter_mixins or self._property_constant_setter_mixins
            else []
        )
