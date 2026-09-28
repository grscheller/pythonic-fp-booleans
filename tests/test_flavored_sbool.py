# Copyright 2023-2026 Geoffrey R. Scheller
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

from pythonic_fp.booleans.flavored import FBool, falsy, truthy
from pythonic_fp.booleans.subtypable import LIE, TRUTH, SBool

fbt0_1 = FBool(2 - 1 == 1, 0)
sbt_1 = SBool(42 == 12 + 30)
fbt1_1 = FBool(42, 1)
sbt_2 = SBool(42)

fbf0_1 = FBool(2 - 1 < 0, 0)
sbf_1 = SBool(42 != 21 * 2)
fbf1_1 = FBool(0, 1)
sbf_2 = SBool('')


class TestIdentiyFBoolEquality:
    def test_identity_fbool(self) -> None:
        # based on identity

        assert fbt0_1 is not sbt_1
        assert fbt1_1 is not sbt_2
        assert fbf0_1 is not sbf_1
        assert fbf1_1 is not sbf_2

        assert fbt0_1 is not fbt1_1
        assert fbt0_1 is not sbt_2
        assert sbt_2 is sbt_1
        assert fbt1_1 is not sbt_1
        assert fbf0_1 is not fbf1_1
        assert fbf0_1 is not sbf_2
        assert sbf_2 is sbf_1
        assert fbf1_1 is not sbf_1

        assert fbt0_1 is truthy(0)
        assert fbt1_1 is truthy(1)
        assert fbt0_1 is not truthy(1)
        assert fbt0_1 is not truthy('foobar')
        assert sbt_1 is TRUTH
        assert sbt_2 is TRUTH
        assert sbt_1 is not LIE
        assert sbt_2 is not LIE
        assert sbf_1 is LIE
        assert sbf_2 is LIE
        assert sbf_1 is not TRUTH
        assert sbf_2 is not TRUTH

    def test_equality_fbool(self) -> None:
        # based on truthiness

        assert fbt0_1 == sbt_1
        assert fbt1_1 == sbt_2
        assert fbf0_1 == sbf_1
        assert fbf1_1 == sbf_2

        assert fbt0_1 == fbt1_1
        assert fbt0_1 == sbt_2
        assert sbt_2 == sbt_1
        assert fbt1_1 == sbt_1
        assert fbf0_1 == fbf1_1
        assert fbf0_1 == sbf_2
        assert sbf_2 == sbf_1
        assert fbf1_1 == sbf_1

        assert fbt0_1 != fbf1_1
        assert fbt0_1 != sbf_2
        assert sbt_2 != sbf_1
        assert fbt1_1 != sbf_1
        assert fbf0_1 != fbt1_1
        assert fbf0_1 != sbt_2
        assert sbf_2 != sbt_1
        assert fbf1_1 != sbt_1


class TestBitwiseOperations:
    def test_or_not(self) -> None:
        assert truthy(0) is (fbt0_1 | fbt0_1)
        assert TRUTH is (sbt_1 | fbt0_1)
        try:
            fbt0_1 | fbt1_1
        except ValueError as err:
            assert (
                str(err) == 'Error: diffent flavored booleans compared with | operator'
            )
        else:
            assert False

    def test_xor_not(self) -> None:
        assert LIE is (fbt0_1 ^ sbt_1)
        assert TRUTH is (fbt0_1 ^ sbf_1)
        assert TRUTH is (sbf_1 ^ fbt0_1)
        assert TRUTH is (fbf0_1 ^ ~sbf_1)

        assert LIE is (fbt0_1 ^ sbt_2)
        assert TRUTH is (fbt0_1 ^ sbf_1)
        assert LIE is (fbf0_1 ^ sbf_1)
        assert TRUTH == (~fbf0_1 ^ sbf_1)
        assert TRUTH == (sbf_1 ^ ~fbf0_1)
        assert TRUTH == (~fbf0_1 ^ sbf_2)
        assert LIE == (fbf1_1 ^ sbf_1)
        assert TRUTH == ~(fbf1_1 ^ sbf_1)

    def test_not(self) -> None:
        assert TRUTH is (fbt0_1 & sbt_1)
        assert LIE is (fbt0_1 & ~sbt_1)
        assert LIE is (~fbt0_1 & sbt_1)
        assert LIE is (~fbt0_1 & ~sbt_1)
        assert TRUTH is ~(~fbt0_1 & ~sbt_1)
        assert TRUTH is ~(~fbt0_1 & sbf_1)
        assert LIE is (fbf0_1 & sbf_1)

        assert TRUTH is (fbt0_1 | sbt_1)
        assert TRUTH is (fbt0_1 | ~sbt_1)
        assert TRUTH is (~fbt0_1 | sbt_1)
        assert LIE is (~fbt0_1 | ~sbt_1)
        assert TRUTH is ~(~fbt0_1 | ~sbt_1)
        assert TRUTH is ~(~fbt1_1 | sbf_2)
        assert LIE is (fbf1_1 | sbf_2)

        assert LIE is (fbt0_1 ^ sbt_1)
        assert TRUTH is (fbt0_1 ^ ~sbt_1)
        assert TRUTH is (~fbt0_1 ^ sbt_1)
        assert LIE is (~fbt0_1 ^ ~sbt_1)
        assert TRUTH is ~(~fbt0_1 ^ ~sbt_1)
        assert TRUTH is ~(~fbt1_1 ^ sbf_2)
        assert LIE is ~(fbt1_1 ^ sbf_2)
        assert LIE is (fbf1_1 ^ sbf_2)

        assert TRUTH is (fbt0_1 & sbt_2)
        assert LIE is (fbt0_1 & ~sbt_2)
        assert LIE is (~fbt0_1 & sbt_2)
        assert LIE is (~fbt0_1 & ~sbt_2)
        assert TRUTH is ~(~fbt0_1 & ~sbt_2)
        assert TRUTH is ~(~fbt1_1 & sbf_1)
        assert LIE is (fbf1_1 & sbf_1)

    def test_de_morgan(self) -> None:
        for fb1 in [truthy(0), falsy(0)]:
            for fb2 in [truthy(0), falsy(0)]:
                assert ~(fb1 & fb2) is (~fb1 | ~fb2)
                assert ~(fb1 | fb2) is (~fb1 & ~fb2)

        for sb1 in [TRUTH, LIE]:
            for fb2 in [truthy(0), falsy(0)]:
                assert ~(sb1 & fb2) is (~sb1 | ~fb2)
                assert ~(sb1 | fb2) is (~sb1 & ~fb2)

        for fb1 in [truthy(0), falsy(0)]:
            for sb2 in [TRUTH, LIE]:
                assert ~(fb1 & sb2) is (~fb1 | ~sb2)
                assert ~(fb1 | sb2) is (~fb1 & ~sb2)
