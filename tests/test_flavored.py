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

from pythonic_fp.booleans.flavored import FBool, truthy, falsy
from pythonic_fp.booleans.subtypable import TRUTH, LIE

t0_1 = FBool(1 == 1, 0)
t0_2 = FBool(42 == 42, 0)
t1_1 = FBool(42, 1)
t1_2 = FBool(42, 1)

f0_1 = FBool(1 < 0, 0)
f0_2 = FBool(42 != 42, 0)
f1_1 = FBool(0, 1)
f1_2 = FBool('', 1)

class TestIdentiyFBoolEquality():
    def test_identity_fbool(self) -> None:
        # based on identity

        t0_1 is t0_1
        t0_1 is t0_2
        t1_2 is t1_2
        t1_1 is t1_2
        f0_1 is f0_1
        f0_1 is f0_2
        f1_2 is f1_2
        f1_1 is f1_2

        t0_1 is not t1_1
        t0_1 is not t1_2
        t1_2 is not t0_2
        t1_1 is not t0_2
        f0_1 is not f1_1
        f0_1 is not f1_2
        f1_2 is not f0_2
        f1_1 is not f0_2

        t0_1 is truthy(0)
        t0_1 is not truthy('foobar')
        t1_2 is not truthy(0)
        t1_2 is truthy(1)
        t1_2 is not falsy(0)
        t1_2 is not falsy(1)

        truthy('foo') is truthy('foo')
        falsy('foo') is falsy('foo')
        truthy('foo') is not truthy('bar')
        falsy('foo') is not falsy('bar')
        truthy('foo') is not falsy('foo')
        truthy('bar') is not falsy('bar')
        truthy('foo') is not falsy('bar')
        truthy('bar') is not falsy('foo')

    def test_equality_fbool(self) -> None:
        # based on truthiness

        t0_1 == t0_1
        t0_1 == t0_2
        t1_2 == t1_2
        t1_1 == t1_2
        f0_1 == f0_1
        f0_1 == f0_2
        f1_2 == f1_2
        f1_1 == f1_2

        t0_1 == t1_1
        t0_1 == t1_2
        t1_2 == t0_2
        t1_1 == t0_2
        f0_1 == f1_1
        f0_1 == f1_2
        f1_2 == f0_2
        f1_1 == f0_2

        t0_1 != f1_1
        t0_1 != f1_2
        t1_2 != f0_2
        t1_1 != f0_2
        f0_1 != t1_1
        f0_1 != t1_2
        f1_2 != t0_2
        f1_1 != t0_2

        truthy('foo') == truthy('foo')
        truthy('foo') == truthy('bar')
        falsy('foo') == falsy('foo')
        falsy('foo') == falsy('bar')
        truthy('foobar') != falsy('foobar')
        truthy('foobar') != falsy('foofoo')

class TestBitwiseOperations():
    def test_or_not(self) -> None:
        assert truthy(0) is (t0_1 | t0_1)
        assert truthy(0) is (t0_2 | t0_1)

    def test_xor_not(self) -> None:
        assert falsy(0) is (t0_1 ^ t0_2)
        assert truthy(0) is (t0_1 ^ f0_2)
        assert truthy(0) is (f0_1 ^ ~f0_2)

        assert truthy(0) is (t0_1 ^ f0_2)
        assert falsy(0) is (f0_1 ^ f0_2)
        assert truthy(0) == (~f0_1 ^ f0_2)

    def test_not(self) -> None:
        assert truthy(0) is (t0_1 & t0_2)
        assert falsy(0) is (t0_1 & ~t0_2)
        assert falsy(0) is (~t0_1 & t0_2)
        assert falsy(0) is (~t0_1 & ~t0_2)
        assert truthy(0) is ~(~t0_1 & ~t0_2)
        assert truthy(0) is ~(~t0_1 & f0_2)
        assert falsy(0) is (f0_1 & f0_2)

        assert truthy(0) is (t0_1 | t0_2)
        assert truthy(0) is (t0_1 | ~t0_2)
        assert truthy(0) is (~t0_1 | t0_2)
        assert falsy(0) is (~t0_1 | ~t0_2)
        assert truthy(0) is ~(~t0_1 | ~t0_2)
        assert truthy(1) is ~(~t1_1 | f1_2)
        assert falsy(1) is (f1_1 | f1_2)

        assert falsy(0) is (t0_1 ^ t0_2)
        assert truthy(0) is (t0_1 ^ ~t0_2)
        assert truthy(0) is (~t0_1 ^ t0_2)
        assert falsy(0) is (~t0_1 ^ ~t0_2)
        assert truthy(0) is ~(~t0_1 ^ ~t0_2)
        assert truthy(1) is ~(~t1_1 ^ f1_2)
        assert falsy(1) is ~(t1_1 ^ f1_2)
        assert falsy(1) is (f1_1 ^ f1_2)

    def test_de_morgan(self) -> None:
        for fb1 in [truthy(0), falsy(0)]:
            for fb2 in [truthy(0), falsy(0)]:
                ~(fb1 & fb2) is (~fb1 | ~fb2)
                ~(fb1 | fb2) is (~fb1 & ~fb2)

        for fb1 in [truthy(1), falsy(1)]:
            for fb2 in [truthy(1), falsy(1)]:
                ~(fb1 & fb2) == (~fb1 | ~fb2)
                ~(fb1 | fb2) == (~fb1 & ~fb2)

        for fb1 in [truthy(()), falsy(())]:
            for fb2 in [truthy(()), falsy(())]:
                ~(fb1 & fb2) == (~fb1 | ~fb2)
                ~(fb1 | fb2) == (~fb1 & ~fb2)
