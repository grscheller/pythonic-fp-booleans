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

from pythonic_fp.booleans.subtypable import SBool, snot, TRUTH, LIE
from pythonic_fp.booleans.subtypes.flavored import FBool, truthy, falsy
from pythonic_fp.booleans.subtypes.true_false import TSBool, FSBool, ALWAYS, NEVER_EVER

class TestShortCutLogic():
    def test_snot_sbool(self) -> None:
        assert snot(SBool(True)) is SBool(False)
        assert snot(SBool(False)) is SBool(True)

    def test_snot_fbool(self) -> None:
        assert snot(FBool(True, 0)) is FBool(False, 0)
        assert snot(FBool(True, 0)) is not FBool(False, 1)

    def test_snot_true_false(self) -> None:
        assert snot(TSBool()) is FSBool()
        assert snot(FSBool()) is TSBool()
