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
from pythonic_fp.booleans.flavored import FBool, truthy, falsy


class TestBitwiseOperations():
    def test_identity(self) -> None:
        assert truthy(0) is truthy(0)
        assert truthy(0) is ~falsy(0)
        assert ~truthy(0) is falsy(0)
        assert ~truthy(0) is falsy(0)

        assert truthy(0) is not truthy(1)
        assert truthy(0) == truthy(1)
        assert falsy(0) is not ~truthy(1)
        assert falsy(0) == ~truthy(1)

        assert FBool('foo', 'bar') is truthy('bar')
        assert FBool('', 'bar') is falsy('bar')

        assert bool(1 == 1) == truthy(0)       # type: ignore
        assert bool(1 == 1) is not truthy(0)   # type: ignore
        assert bool(1 == 0) == ~truthy(0)      # type: ignore
        assert bool(1 == 0) is not ~truthy(0)  # type: ignore
        assert TRUTH == truthy(0) == truthy(1)
        assert TRUTH is not truthy(0)
        assert TRUTH is not truthy(1)
        assert truthy(0) is not truthy(1)
        assert LIE == falsy(0) == falsy(1)
        assert LIE is not falsy(0)
        assert LIE is not falsy(1)
        assert falsy(0) is not falsy(1)

    def test_or_not(self) -> None:
        assert truthy(0) is truthy(0) | truthy(0)
        assert truthy(0) is truthy(0) | ~truthy(0)
        assert truthy(0) is ~truthy(0) | truthy(0)
        assert falsy(0) is ~truthy(0) | ~truthy(0)

        assert truthy(1) is ~falsy(1) | falsy(1)
        assert truthy(1) is truthy(1) | ~falsy(1)
        assert truthy(1) is ~falsy(1) | truthy(1)
        assert falsy(1) is ~truthy(1) | ~truthy(1)

        assert falsy(0) is falsy(0) | falsy(0)
        assert truthy(1) is falsy(1) | ~falsy(1)
        assert truthy(0) is ~falsy(0) | falsy(0)
        assert truthy(1) is ~falsy(1) | ~falsy(1)

        assert TRUTH is truthy(0) | TRUTH
        assert TRUTH == TRUTH | truthy(1)
        assert TRUTH is truthy(0) | LIE
        assert TRUTH == LIE | truthy(1)
        assert TRUTH is falsy(0) | TRUTH
        assert TRUTH == TRUTH | falsy(1)
        assert LIE is falsy(0) | LIE
        assert LIE == LIE | falsy(1)

    def test_and_not(self) -> None:
        assert truthy(0) is truthy(0) & truthy(0)
        assert falsy(0) is truthy(0) & ~truthy(0)
        assert falsy(0) is ~truthy(0) & truthy(0)
        assert falsy(0) is ~truthy(0) & ~truthy(0)

        assert falsy(1) is ~falsy(1) & falsy(1)
        assert truthy(1) is truthy(1) & ~falsy(1)
        assert truthy(1) is ~falsy(1) & truthy(1)
        assert falsy(1) is ~truthy(1) & ~truthy(1)

        assert falsy(0) is falsy(0) & falsy(0)
        assert falsy(1) is falsy(1) & ~falsy(1)
        assert falsy(0) is ~falsy(0) & falsy(0)
        assert truthy(1) is ~falsy(1) & ~falsy(1)

        assert TRUTH is truthy(0) & TRUTH
        assert TRUTH == TRUTH & truthy(1)
        assert LIE is truthy(0) & LIE
        assert LIE == LIE & truthy(1)
        assert LIE is falsy(0) & TRUTH
        assert LIE == TRUTH & falsy(1)
        assert LIE is falsy(0) & LIE
        assert LIE == LIE & falsy(1)

    def test_xor_not(self) -> None:
        assert falsy(0) is truthy(0) ^ truthy(0)
        assert truthy(0) is truthy(0) ^ ~truthy(0)
        assert truthy(0) is ~truthy(0) ^ truthy(0)
        assert falsy(0) is ~truthy(0) ^ ~truthy(0)

        assert truthy(1) is ~falsy(1) ^ falsy(1)
        assert falsy(1) is truthy(1) ^ ~falsy(1)
        assert falsy(1) is ~falsy(1) ^ truthy(1)
        assert falsy(1) is ~truthy(1) ^ ~truthy(1)

        assert falsy(0) is falsy(0) ^ falsy(0)
        assert truthy(1) is falsy(1) ^ ~falsy(1)
        assert truthy(0) is ~falsy(0) ^ falsy(0)
        assert falsy(1) is ~falsy(1) ^ ~falsy(1)

        assert LIE is truthy(0) ^ TRUTH
        assert LIE == TRUTH ^ truthy(1)
        assert TRUTH is truthy(0) ^ LIE
        assert TRUTH == LIE ^ truthy(1)
        assert TRUTH is falsy(0) ^ TRUTH
        assert TRUTH == TRUTH ^ falsy(1)
        assert LIE is falsy(0) ^ LIE
        assert LIE == LIE ^ falsy(1)

    def test_de_morgan(self) -> None:
        lie1 = falsy(1)
        lie2 = falsy(2)
        truth1 = truthy(1)
        truth2 = truthy(2)

        for b1 in [truth1, lie1]:
            for b2 in [truth1, lie1]:
                ~(b1 & b2) is ~b1 | ~b2
                ~(b1 | b2) is ~b1 & ~b2

        for b1 in [truth2, lie2]:
            for b2 in [truth2, lie2]:
                ~(b1 & b2) is ~b1 | ~b2
                ~(b1 | b2) is ~b1 & ~b2
