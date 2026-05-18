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
from pythonic_fp.booleans.truthy_falsy import TF_Bool, T_Bool, F_Bool
from pythonic_fp.booleans.truthy_falsy import ALWAYS, NEVER

class TestBitwiseOperations():
    def test_identity(self) -> None:
        assert TF_Bool(0) is F_Bool()
        assert TF_Bool(1) is T_Bool()
        assert ~TF_Bool('foo') is F_Bool()
        assert ~TF_Bool('') is T_Bool()
        assert TF_Bool('foo') is ~F_Bool()
        assert TF_Bool('') is ~T_Bool()
        assert TF_Bool('') is TF_Bool(0)

        assert bool(1 == 1) == TF_Bool(42)      # type: ignore
        assert bool(1 == 1) is not TF_Bool(42)  # type: ignore
        assert bool(1 == 0) == ~T_Bool()        # type: ignore
        assert bool(1 == 0) == F_Bool()         # type: ignore
        assert bool(1 == 0) is not F_Bool()     # type: ignore
        assert bool(1 == 0) is not ~T_Bool()    # type: ignore
        assert TRUTH == ~LIE
        assert LIE == ~TRUTH
        assert TRUTH == ALWAYS
        assert TRUTH is not ALWAYS
        assert LIE == NEVER
        assert LIE is not NEVER

    def test_or_not(self) -> None:
        assert ALWAYS is ALWAYS | ALWAYS
        assert ALWAYS is ALWAYS | ~ALWAYS
        assert ALWAYS is ~ALWAYS | ALWAYS
        assert NEVER is ~ALWAYS | ~ALWAYS

        assert NEVER is NEVER | NEVER
        assert ALWAYS is NEVER | ~NEVER
        assert ALWAYS is ~NEVER | NEVER
        assert ALWAYS is ~NEVER | ~NEVER

        assert NEVER is NEVER | ~ALWAYS
        assert ALWAYS is ALWAYS | ~NEVER
        assert NEVER is ~ALWAYS | NEVER
        assert ALWAYS is ~NEVER | ~ALWAYS

        assert TRUTH is ALWAYS | TRUTH
        assert TRUTH is TRUTH | ALWAYS
        assert TRUTH is ALWAYS | LIE
        assert TRUTH is LIE | ALWAYS
        assert LIE is NEVER | LIE
        assert LIE is LIE | NEVER
        assert TRUTH is TRUTH | NEVER
        assert TRUTH is NEVER | TRUTH

    def test_and_not(self) -> None:
        assert ALWAYS is ALWAYS & ALWAYS
        assert NEVER is ALWAYS & ~ALWAYS
        assert NEVER is ~ALWAYS & ALWAYS
        assert NEVER is ~ALWAYS & ~ALWAYS

        assert NEVER is NEVER & NEVER
        assert NEVER is NEVER & ~NEVER
        assert NEVER is ~NEVER & NEVER
        assert ALWAYS is ~NEVER & ~NEVER

        assert NEVER is NEVER & ~ALWAYS
        assert ALWAYS is ALWAYS & ~NEVER
        assert NEVER is ~ALWAYS & NEVER
        assert NEVER is ~NEVER & ~ALWAYS

        assert TRUTH is ALWAYS & TRUTH
        assert TRUTH is TRUTH & ALWAYS
        assert LIE is ALWAYS & LIE
        assert LIE is LIE & ALWAYS
        assert LIE is NEVER & LIE
        assert LIE is LIE & NEVER
        assert LIE is TRUTH & NEVER
        assert LIE is NEVER & TRUTH

    def test_xor_not(self) -> None:
        assert NEVER is ALWAYS ^ ALWAYS
        assert ALWAYS is ALWAYS ^ ~ALWAYS
        assert ALWAYS is ~ALWAYS ^ ALWAYS
        assert NEVER is ~ALWAYS ^ ~ALWAYS

        assert NEVER is NEVER ^ NEVER
        assert ALWAYS is NEVER ^ ~NEVER
        assert ALWAYS is ~NEVER ^ NEVER
        assert NEVER is ~NEVER ^ ~NEVER

        assert NEVER is NEVER ^ ~ALWAYS
        assert NEVER is ALWAYS ^ ~NEVER
        assert NEVER is ~ALWAYS ^ NEVER
        assert ALWAYS is ~NEVER ^ ~ALWAYS

        assert LIE is ALWAYS ^ TRUTH
        assert LIE is TRUTH ^ ALWAYS
        assert TRUTH is ALWAYS ^ LIE
        assert TRUTH is LIE ^ ALWAYS
        assert LIE is NEVER ^ LIE
        assert LIE is LIE ^ NEVER
        assert TRUTH is TRUTH ^ NEVER
        assert TRUTH is NEVER ^ TRUTH

    def test_de_morgan(self) -> None:
        for tfb in [NEVER, ALWAYS]:
            for tf2 in [NEVER, ALWAYS]:
                ~(tfb & tf2) is ~tfb | ~tf2
                ~(tfb | tf2) is ~tfb & ~tf2
