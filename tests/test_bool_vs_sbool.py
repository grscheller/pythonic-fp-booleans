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

from pythonic_fp.booleans.subtypable.sbool import SBool, snot, TRUTH, LIE

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

        foo = 42
        bool1 = bool(foo == 1)
        bool2 = bool(foo != 42)
        tup: tuple[int, ...] = (bool1 and (foo, 42) or bool2 and (foo, foo, 42)) or ()
        assert tup == ()

        foo = 0
        bool1 = bool(foo == 1)
        bool2 = bool(foo != 42)
        tup = (bool1 and (foo, 42) or bool2 and (foo, foo, 42)) or ()
        assert tup == (0, 0, 42)

        foo = 1
        bool1 = bool(foo == 1)
        bool2 = bool(foo != 42)
        tup = (bool1 and (foo, 42) or bool2 and (foo, foo, 42)) or ()
        assert tup == (1, 42)

        bool1 = True
        bool2 = False
        bool1 is bool1
        bool2 is bool2
        bool1 is not bool2
        bool1 == (not bool2)
        bool2 == (not bool1)

    def test_sbool(self) -> None:
        # Next make sure that SBool does the same
        sbool_t1 = TRUTH
        sbool_t2 = SBool(1)

        sbool_f1 = LIE
        sbool_f2 = SBool(0)

        assert sbool_t1 == sbool_t2
        assert sbool_t1 is sbool_t2

        assert sbool_f1 == sbool_f2
        assert sbool_f1 is sbool_f2

        foo = 42
        sbool1 = SBool(foo == 1)
        sbool2 = SBool(foo != 42)
        tup: tuple[int, ...] = (sbool1 and (foo, 42) or sbool2 and (foo, foo, 42)) or ()
        assert tup == ()

        foo = 0
        sbool1 = SBool(foo == 1)
        sbool2 = SBool(foo != 42)
        tup = (sbool1 and (foo, 42) or sbool2 and (foo, foo, 42)) or ()
        assert tup == (0, 0, 42)

        foo = 1
        sbool1 = SBool(foo == 1)
        sbool2 = SBool(foo != 42)
        tup = (sbool1 and (foo, 42) or sbool2 and (foo, foo, 42)) or ()
        assert tup == (1, 42)

        sbool1 = TRUTH
        sbool2 = LIE
        sbool1 is sbool1
        sbool2 is sbool2
        sbool1 is not sbool2
        sbool1 == snot(sbool2)
        sbool2 == snot(sbool1)
        # Why we need snot
        True is (not LIE)
        False is (not TRUTH)
