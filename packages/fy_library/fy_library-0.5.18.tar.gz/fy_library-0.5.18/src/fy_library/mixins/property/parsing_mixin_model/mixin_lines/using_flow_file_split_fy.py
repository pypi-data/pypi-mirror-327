# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""fy
from typing import List


property mixin_lines: List[str] using flow_file_split:
    property flow_file_split
fy"""

import abc
from functools import cached_property
from typing import List

from fy_library.mixins.property.parsed_file_split.flow_file_split.abc_fy import (
    FlowFileSplit_PropertyMixin_ABC,
)
from fy_library.mixins.property.parsing_mixin_model.mixin_lines.abc_fy import (
    MixinLines_PropertyMixin_ABC,
)


# fy:start ===>>>
class MixinLines_UsingFlowFileSplit_PropertyMixin(
    # Property Mixins
    FlowFileSplit_PropertyMixin_ABC,
    MixinLines_PropertyMixin_ABC,
    abc.ABC,
):
    @cached_property
    def _mixin_lines(self) -> List[str]:
        # fy:end <<<===
        return self._flow_file_split.mixins.split("\n")
