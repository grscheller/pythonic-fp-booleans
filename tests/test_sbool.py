# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pythonic_fp.gadgets.lca import latest_common_ancestor as lca
from pythonic_fp.booleans.sbool import SBool, snot, TRUTH, LIE

class TestBooleanBehaviors():
    def test_bool(self) -> None:
        # First make sure we understand what bool does
        bool_t1 = True
        bool_t2 = bool(42)

        bool_f1 = False
        bool_f2 = bool(0)

        assert bool_t1 == bool_t2
        assert bool_t1 is bool_t2

        assert bool_f1 == bool_f2
        assert bool_f1 is bool_f2

    def test_sbool(self) -> None:
        # Make sure that SBool does the same
        sbool_t1 = TRUTH
        sbool_t2 = SBool(1)

        sbool_f1 = LIE
        sbool_f2 = SBool(0)

        assert sbool_t1 == sbool_t2
        # assert sbool_t1 is sbool_t2   # Opps, not a singleton!

        assert sbool_f1 == sbool_f2
        # assert sbool_f1 is sbool_f2
