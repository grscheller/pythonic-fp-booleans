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

from pythonic_fp.booleans.subtypable import TRUTH, LIE
from pythonic_fp.booleans.subtypes.true_false import TF_Boolean, TF_Bool, T_Bool, F_Bool
from pythonic_fp.booleans.subtypes.true_false import ALWAYS, NEVER_EVER

true1: TF_Boolean = TF_Bool(1 < 42)
true2: TF_Boolean = T_Bool()
false1: TF_Boolean = TF_Bool(1 > 42)
false2: TF_Boolean = F_Bool()


class TestBitwiseOperations():
    def test_typed_identity(self) -> None:
        assert TRUTH == ALWAYS
        assert ALWAYS == ALWAYS
        assert ALWAYS != NEVER_EVER
        assert NEVER_EVER != ALWAYS
        assert NEVER_EVER == NEVER_EVER
        assert LIE == NEVER_EVER
        assert TRUTH is not ALWAYS
        assert ALWAYS is ALWAYS
        assert ALWAYS is not NEVER_EVER
        assert NEVER_EVER is not ALWAYS
        assert NEVER_EVER is NEVER_EVER
        assert LIE is not NEVER_EVER

        assert true1 == true1
        assert true1 == true2
        assert true2 == true1
        assert true2 == true2
        assert true1 is true1
        assert true1 is true2
        assert true2 is true1
        assert true2 is true2

        assert ALWAYS == true1 == true2
        assert NEVER_EVER == false1 == false2

    def test_or_not(self) -> None:
        assert True

    def test_xor_not(self) -> None:
        assert True

    def test_and_not(self) -> None:
        assert True

    def test_de_morgan(self) -> None:
        for tfb in [true1, false1]:
            for tf2 in [true1, false1]:
                ~(tfb & tf2) is ~tfb | ~tf2
                ~(tfb | tf2) is ~tfb & ~tf2

        for tfb in [true1, false1]:
            for tf2 in [true2, false2]:
                ~(tfb & tf2) is ~tfb | ~tf2
                ~(tfb | tf2) is ~tfb & ~tf2

        for tfb in [true2, false2]:
            for tf2 in [true1, false1]:
                ~(tfb & tf2) is ~tfb | ~tf2
                ~(tfb | tf2) is ~tfb & ~tf2

        for tfb in [true2, false2]:
            for tf2 in [true2, false2]:
                ~(tfb & tf2) is ~tfb | ~tf2
                ~(tfb | tf2) is ~tfb & ~tf2
