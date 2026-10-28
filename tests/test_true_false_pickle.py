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

"""Pickle tests for truthy_falsy booleans."""

import copy
import pickle
import subprocess
import sys

from pythonic_fp.booleans.truthy_falsy import ALWAYS, NEVER, F_Bool, T_Bool, TF_Bool

tbool: TF_Bool = T_Bool()
fbool: TF_Bool = F_Bool()


class TestBooleanPickle:
    def test_equalitY_survives_all_protocols(self) -> None:
        for item in ALWAYS, NEVER, tbool, fbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored == item, f'protocol {protocol} made an unequal copy'

    def test_identity_survives_all_protocols(self) -> None:
        for item in ALWAYS, NEVER, tbool, fbool:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(item, protocol=protocol))
                assert restored is item, f'protocol {protocol} made a new instance'

    def test_identity_with_TF_Bool_constructor(self) -> None:
        truthy, falsy = TF_Bool({'one': 1, 'two': 2}), TF_Bool({})
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_truthy, r_falsy = pickle.loads(
                pickle.dumps((truthy, falsy), protocol=protocol)
            )
            assert r_truthy is ALWAYS
            assert r_falsy is NEVER
            assert r_truthy is truthy
            assert r_falsy is falsy
            assert truthy is not falsy

    def test_identity_inside_containers(self) -> None:
        payload = {'a': [tbool], 'b': (fbool, ALWAYS), 'c': NEVER}
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            restored = pickle.loads(pickle.dumps(payload, protocol=protocol))
            assert restored['a'][0] is tbool
            assert restored['b'][0] is fbool
            assert restored['b'][1] is ALWAYS
            assert restored['c'] is NEVER

    def test_copy_and_deepcopy_return_the_singleton(self) -> None:
        t1 = TF_Bool(1 + 1 == 2)
        f1 = TF_Bool(1 + 1 == 42)
        t2 = T_Bool()
        f2 = F_Bool()
        assert copy.copy(t1) is t1
        assert copy.copy(f1) is f1
        assert copy.deepcopy(t1) is t1
        assert copy.deepcopy(f1) is f1
        assert copy.deepcopy(t2) is t2
        assert copy.deepcopy(f2) is f2
        assert t1 is t2
        assert f1 is f2

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
        _SCRIPT = """
        import pickle, sys
        from pythonic_fp.booleans.truthy_falsy import F_Bool, T_Bool, TF_Bool
        restored = pickle.loads(sys.stdin.buffer.read())
        assert restored[0] is T_Bool(), 'truthy came back as a duplicate'
        assert restored[1] is F_Bool(), 'falsy came back as a duplicate'
        assert restored[2] is T_Bool(), 'truthy came back as a duplicate'
        assert restored[3] is F_Bool(), 'falsy came back as a duplicate'
        assert restored[4] is T_Bool(), 'truthy came back as a duplicate'
        assert restored[5] is F_Bool(), 'falsy came back as a duplicate'
        assert restored[6] is TF_Bool([1, 2, 3]), 'truthy came back as a duplicate'
        assert restored[7] is TF_Bool(()), 'falsy came back as a duplicate'
        print('ok')
        """

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            blob = pickle.dumps(
                (
                    tbool,
                    fbool,
                    TF_Bool(42),
                    TF_Bool(0),
                    TF_Bool('foobar'),
                    TF_Bool(''),
                    TF_Bool(['foo', 'bar']),
                    TF_Bool([]),
                ),
                protocol=protocol,
            )
            done = self._run(_SCRIPT, blob)
            assert done.stdout.strip() == b'ok', f'protocol {protocol}'
