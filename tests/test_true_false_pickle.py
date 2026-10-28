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

import pytest

from pythonic_fp.booleans.truthy_falsy import ALWAYS, NEVER, F_Bool, T_Bool, TF_Bool

tbool: TF_Bool = T_Bool()
fbool: TF_Bool = F_Bool()


class TestSentinelPickle:
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

    def test_identity_with_TS_Bool_constructor(self) -> None:
        truthy, falsy = TF_Bool(True), TF_Bool(False)
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            r_truthy, r_falsy = pickle.loads(pickle.dumps((truthy, falsy)))
            assert r_truthy is ALWAYS
            assert r_falsy is NEVER
            assert r_truthy is truthy
            assert r_falsy is falsy
            assert truthy is not falsy

#   def test_identity_inside_containers(self) -> None:
#       sentinel = Sentinel('alpha')
#       payload = {'one': [sentinel], 'two': (sentinel, sentinel)}
#       restored = pickle.loads(pickle.dumps(payload))
#       assert restored['one'][0] is sentinel
#       assert restored['two'][0] is sentinel
#       assert restored['two'][1] is sentinel

#   def test_copy_and_deepcopy_return_the_singleton(self) -> None:
#       sentinel = Sentinel('alpha')
#       assert copy.copy(sentinel) is sentinel
#       assert copy.deepcopy(sentinel) is sentinel

#   def test_identity_in_a_fresh_interpreter(self) -> None:
#       """A sentinel unpickled in a new process is that process's singleton."""
#       blob = pickle.dumps(Sentinel('alpha'))
#       script = (
#           'import pickle, sys\n'
#           'from pythonic_fp.gadgets.sentinels.flavored import Sentinel\n'
#           'restored = pickle.loads(sys.stdin.buffer.read())\n'
#           "assert restored is Sentinel('alpha')\n"
#           "assert restored.flavor() == 'alpha'\n"
#           "print('ok')\n"
#       )
#       done = subprocess.run(
#           [sys.executable, '-c', script], input=blob,
#           capture_output=True, check=True,
#       )
#       assert done.stdout.strip() == b'ok'

#   def test_unhashable_flavor_rejected(self) -> None:
#       with pytest.raises(TypeError):
#           Sentinel(([1, 2],))

#   def test_repr_reproduces_the_sentinel(self) -> None:
#       sentinel = Sentinel('alpha')
#      assert eval(repr(sentinel)) is sentinel
