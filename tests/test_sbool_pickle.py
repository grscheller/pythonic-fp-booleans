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

"""Pickle tests for subtypable booleans."""

import pickle
import subprocess
import sys
from collections.abc import Hashable
from copy import copy, deepcopy
from threading import Lock
from typing import ClassVar, Self, cast, overload

from pythonic_fp.gadgets.sentinels.novalue import NoValue

from pythonic_fp.booleans.subtypable import LIE, TRUTH, SBool

no_value = NoValue()

tsbool: SBool = SBool('not empty')
fsbool: SBool = SBool('')


class TestSBoolPickle:
    def test_int_value_survives_all_protocols(self) -> None:
        """SBool inherits int.__eq__, so this compares the
        integer payload, not identity. A duplicated singleton still
        compares equal -- test_identity_survives_all_protocols covers
        that. What this catches is a __reduce__ that reconstructs the
        wrong class.
        """
        for item in TRUTH, LIE, tsbool, fsbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored == item, f'protocol {protocol} made an unequal copy'

    def test_identity_survives_all_protocols(self) -> None:
        for item in TRUTH, LIE, tsbool, fsbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_identity_with_SBool_constructor(self) -> None:
        truthy, falsy = SBool({'one': 1, 'two': 2}), SBool({})
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_truthy, r_falsy = pickle.loads(
                pickle.dumps((truthy, falsy), protocol=protocol)
            )
            assert r_truthy is TRUTH
            assert r_falsy is LIE
            assert r_truthy is truthy
            assert r_falsy is falsy
            assert truthy is not falsy

    def test_identity_inside_containers(self) -> None:
        payload = {'a': [tsbool], 'b': (fsbool, TRUTH), 'c': LIE}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is tsbool
            assert restored['b'][0] is fsbool
            assert restored['b'][1] is TRUTH
            assert restored['c'] is LIE

    def test_copy_and_deepcopy_return_the_singletons(self) -> None:
        t1 = SBool(1 + 1 == 2)
        f1 = SBool(1 + 1 == 42)
        t2 = SBool('foo')
        f2 = SBool('')
        assert copy(t1) is t1
        assert copy(f1) is f1

        type ThingType = tuple[SBool, list[dict[int, SBool]]]
        thing1: ThingType = (t1, [{21: f1, 42: t2}, {7: f2}])
        thing2 = deepcopy(thing1)
        assert thing2[0] is t1
        assert thing2[1][0][21] is f1
        assert thing2[1][0][42] is t2
        assert thing2[1][1][7] is f2
        assert t1 is t2
        assert f1 is f2
        assert thing1 == thing2

    @staticmethod
    def _run(script: str, data: bytes) -> subprocess.CompletedProcess[bytes]:
        done = subprocess.run(
            [sys.executable, '-c', script],
            input=data,
            capture_output=True,
            check=False,
        )
        assert done.returncode == 0, (
            f'child process failed:\n{done.stderr.decode(errors="replace")}'
        )
        return done

    def test_identity_in_a_fresh_interpreter(self) -> None:
        # Remove additional whitespace below if tested on Python <3.14
        _SCRIPT = """
        import pickle, sys
        from pythonic_fp.booleans.subtypable import SBool, TRUTH, LIE
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is TRUTH, 'truthy came back as a duplicate'
        assert restored[1] is LIE, 'falsy came back as a duplicate'
        assert restored[2] is TRUTH, 'truthy came back as a duplicate'
        assert restored[3] is LIE, 'falsy came back as a duplicate'
        assert restored[4] is TRUTH, 'truthy came back as a duplicate'
        assert restored[5] is LIE, 'falsy came back as a duplicate'
        assert restored[6] is SBool([1, 2, 3]), 'truthy came back as a duplicate'
        assert restored[7] is SBool(()), 'falsy came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    tsbool,
                    fsbool,
                    SBool(42),
                    SBool(0),
                    SBool('foobar'),
                    SBool(''),
                    SBool(['foo', 'bar']),
                    SBool([]),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'


class DBool(SBool):
    _false_one: ClassVar[SBool | NoValue] = NoValue()
    _false_one_lock: ClassVar[Lock] = Lock()

    _true_one: ClassVar[SBool | NoValue] = NoValue()
    _true_one_lock: ClassVar[Lock] = Lock()

    @overload
    def __new__(cls, witness: object) -> Self: ...
    @overload
    def __new__(
        cls, witness: object, flavor: Hashable | NoValue = no_value
    ) -> Self: ...

    def __new__(
        cls,
        witness: object,
        flavor: Hashable | NoValue = no_value,
    ) -> Self:
        """
        .. admonition:: new

            :param witness: Determines truthiness of the ``SBool``.
            :param flavor: Ignored, here for Liskov  substitution principle
            :returns: The truthy or falsy ``SBool`` class instance.

        """
        if witness:
            if cls._true_one is NoValue():
                with cls._true_one_lock:
                    if cls._true_one is NoValue():
                        cls._true_one = super().__new__(cls, 1)
            return cast(Self, cls._true_one)
        else:
            if cls._false_one is NoValue():
                with cls._false_one_lock:
                    if cls._false_one is NoValue():
                        cls._false_one = super().__new__(cls, 0)
            return cast(Self, cls._false_one)


tdbool: DBool = DBool(42)
fdbool: DBool = DBool(0)

class TestSubtypedSBoolPickle:
    def test_int_value_survives_all_protocols(self) -> None:
        """DBool inherits int.__eq__, so this compares the
        integer payload, not identity. A duplicated singleton still
        compares equal -- test_identity_survives_all_protocols covers
        that. What this catches is a __reduce__ that reconstructs the
        wrong class.
        """
        for item in tdbool, fdbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored == item, f'protocol {protocol} made an unequal copy'

    def test_subtype_identity_survives_all_protocols(self) -> None:
        for item in tdbool, fdbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_identity_with_DBool_constructor(self) -> None:
        true_one, false_one = DBool({'one': 1, 'two': 2}), DBool({})
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_true_one, r_false_one = pickle.loads(
                pickle.dumps((true_one, false_one), protocol=protocol)
            )
            assert r_true_one is true_one
            assert r_false_one is false_one
            assert r_true_one is true_one
            assert r_false_one is false_one
            assert true_one is not false_one

    def test_identity_inside_containers(self) -> None:
        payload = {'a': [tdbool], 'b': (fdbool, 42.0), 'c': 0.0}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is tdbool
            assert restored['b'][0] is fdbool
            assert restored['b'][1] == 42.0
            assert restored['c'] == 0.0

    def test_copy_and_deepcopy_return_the_singletons(self) -> None:
        t1 = DBool(1 + 1 == 2)
        f1 = DBool(1 + 1 == 42)
        t2 = DBool('foo')
        f2 = DBool('')
        assert copy(t1) is t1
        assert copy(f1) is f1

        type ThingType = tuple[DBool, list[dict[int, DBool]]]
        thing1: ThingType = (t1, [{21: f1, 42: t2}, {7: f2}])
        thing2 = deepcopy(thing1)
        assert thing2[0] is t1
        assert thing2[1][0][21] is f1
        assert thing2[1][0][42] is t2
        assert thing2[1][1][7] is f2
        assert t1 is t2
        assert f1 is f2
        assert thing1 == thing2

    @staticmethod
    def _run(script: str, data: bytes) -> subprocess.CompletedProcess[bytes]:
        done = subprocess.run(
            [sys.executable, '-c', script],
            input=data,
            capture_output=True,
            check=False,
        )
        assert done.returncode == 0, (
            f'child process failed:\n{done.stderr.decode(errors="replace")}'
        )
        return done

    def test_identity_in_a_fresh_interpreter(self) -> None:
        # Remove additional whitespace below if tested on Python <3.14
        _SCRIPT = """
        import pickle, sys
        from . import DBool
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is DBool('string'), 'true_one came back as a duplicate'
        assert restored[1] is DBool(''), 'false_one came back as a duplicate'
        assert restored[2] is DBool(True), 'true_one came back as a duplicate'
        assert restored[3] is DBool(False), 'false_one came back as a duplicate'
        assert restored[4] is DBool((1,2,3)), 'true_one came back as a duplicate'
        assert restored[5] is DBool(()), 'false_one came back as a duplicate'
        assert restored[6] is DBool([1, 2, 3]), 'true_one came back as a duplicate'
        assert restored[7] is DBool([]), 'false_one came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    tdbool,
                    fdbool,
                    DBool(42),
                    DBool(0),
                    DBool('foobar'),
                    DBool(''),
                    DBool(['foo', 'bar']),
                    DBool([]),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'
