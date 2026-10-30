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

import os
import pickle
import subprocess
import sys
from copy import copy, deepcopy

from pythonic_fp.booleans.subtypable import LIE, TRUTH, SBool

from .sbool_pickle_helper import NO, YES, DBool

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
        # Remove leading whitespace below if tested on Python <3.14
        _SCRIPT = """
        import pickle, sys
        from pythonic_fp.booleans.subtypable import SBool, TRUTH, LIE
        from tests.sbool_pickle_helper import DBool, YES, NO
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is TRUTH, 'TRUTH came back as a duplicate'
        assert restored[1] is LIE, 'LIE came back as a duplicate'
        assert restored[2] is TRUTH, 'tsbool came back as a duplicate'
        assert restored[3] is LIE, 'fsbool came back as a duplicate'
        assert restored[4] is TRUTH, 'truthy value came back as a duplicate'
        assert restored[5] is LIE, 'falsy value came back as a duplicate'
        assert restored[6] is TRUTH, 'non-empty value came back as a duplicate'
        assert restored[7] is LIE, 'empty value came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    TRUTH,
                    LIE,
                    tsbool,
                    fsbool,
                    SBool(42),
                    SBool(0),
                    SBool('foobar'),
                    SBool(''),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'


tdbool: DBool = DBool(42)
fdbool: DBool = DBool(0)


class TestSubtypedSBoolInstancesDistinct:
    def test_identities(self) -> None:
        assert tsbool is not tdbool
        assert fsbool is not fdbool
        assert tsbool is not fdbool
        assert fsbool is not tdbool
        assert tsbool is not fsbool
        assert fsbool is not tsbool
        assert tdbool is not fdbool
        assert fdbool is not tdbool


class TestSubtypedSBoolPickle:
    def test_subtyped_int_value_survives_all_protocols(self) -> None:
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

    def test_subtyped_identity_survives_all_protocols(self) -> None:
        for item in tdbool, fdbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_subtyped_identity_with_DBool_constructor(self) -> None:
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

    def test_subtyped_identity_inside_containers(self) -> None:
        payload = {'a': [tdbool], 'b': (fdbool, 42.0), 'c': 0.0}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is tdbool
            assert restored['b'][0] is fdbool
            assert restored['b'][1] == 42.0
            assert restored['c'] == 0.0

    def test_subtyped_copy_and_deepcopy_return_the_singletons(self) -> None:
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

    def test_subtype_identity_in_a_fresh_interpreter(self) -> None:
        _TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

        # Remove leading whitespace below if tested on Python <3.14
        _SCRIPT = f"""
        import pickle, sys
        sys.path.insert(0, {_TESTS_DIR!r})
        from sbool_pickle_helper import NO, YES, DBool
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is YES, 'YES came back as a duplicate'
        assert restored[1] is NO, 'NO came back as a duplicate'
        assert restored[2] is YES, 'tdbool came back as a duplicate'
        assert restored[3] is NO, 'fdbool came back as a duplicate'
        assert restored[4] is YES, 'truthy value came back as a duplicate'
        assert restored[5] is NO, 'falsy value came back as a duplicate'
        assert restored[6] is YES, 'non-empty came back as a duplicate'
        assert restored[7] is NO, 'empty came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    YES,
                    NO,
                    tdbool,
                    fdbool,
                    DBool(42),
                    DBool(0),
                    DBool(['not', 'empty']),
                    DBool([]),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'
