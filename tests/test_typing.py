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

from pythonic_fp.booleans.subtypable import SBool, snot, TRUTH, LIE
from pythonic_fp.booleans.subtypes.flavored import FBool, truthy, falsy
from pythonic_fp.booleans.subtypes.true_false import TFSBool, TSBool, FSBool, ALWAYS, NEVER_EVER

class TestSnot():
    def test_sbool(self) -> None:
        assert snot(SBool(True)) is SBool(False)
        assert snot(SBool(False)) is SBool(True)

    def test_fbool(self) -> None:
        assert snot(FBool(True, 0)) is FBool(False, 0)
        assert snot(FBool(True, 0)) is not FBool(False, 1)
        assert snot(FBool(False, 0)) is FBool(True, 0)
        assert snot(FBool(False, 0)) is not FBool(True, 1)

        assert snot(FBool(False, 'foo') & FBool(False, 'foo')) is FBool(True, 'foo')
        assert snot(FBool(True, 'foo') & FBool(False, 'foo')) is FBool(True, 'foo')
        assert snot(FBool(False, 'foo') & FBool(True, 'foo')) is FBool(True, 'foo')
        assert snot(FBool(True, 'foo') & FBool(True, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(False, 'foo') | FBool(False, 'foo')) is FBool(True, 'foo')
        assert snot(FBool(True, 'foo') | FBool(False, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(False, 'foo') | FBool(True, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(True, 'foo') | FBool(True, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(False, 'foo') ^ FBool(False, 'foo')) is FBool(True, 'foo')
        assert snot(FBool(True, 'foo') ^ FBool(False, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(False, 'foo') ^ FBool(True, 'foo')) is FBool(False, 'foo')
        assert snot(FBool(True, 'foo') ^ FBool(True, 'foo')) is FBool(True, 'foo')

        assert snot(FBool(False, 'foo') & FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') & FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(False, 'foo') & FBool(True, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') & FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(False, 'foo') | FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') | FBool(False, 'bar')) is SBool(False)
        assert snot(FBool(False, 'foo') | FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(True, 'foo') | FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(False, 'foo') ^ FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') ^ FBool(False, 'bar')) is SBool(False)
        assert snot(FBool(False, 'foo') ^ FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(True, 'foo') ^ FBool(True, 'bar')) is SBool(True)

        assert snot(truthy(42)) is falsy(42)
        assert snot(falsy(42)) is truthy(42)
        assert snot(truthy(42)) is not falsy(1)
        assert snot(falsy(42)) is not truthy(1)

    def test_true_false(self) -> None:
        # Not sure why mypy does not like the first two, snot returns
        # an SBool and TSBool and FSBool are both SBool subtypes.
        assert snot(TSBool()) is FSBool()
        assert snot(FSBool()) is TSBool()
        assert snot(TFSBool(True)) is TFSBool(False)
        assert snot(TFSBool(False)) is TFSBool(True)

    def test_sbool_fbool(self) -> None:
        assert snot(SBool(False) & FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') & SBool(False)) is SBool(True)
        assert snot(SBool(False) & FBool(True, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') & SBool(True)) is SBool(False)
        assert snot(SBool(False) | FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') | SBool(False)) is SBool(False)
        assert snot(SBool(False) | FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(True, 'foo') | SBool(True)) is SBool(False)
        assert snot(SBool(False) ^ FBool(False, 'bar')) is SBool(True)
        assert snot(FBool(True, 'foo') ^ SBool(False)) is SBool(False)
        assert snot(SBool(False) ^ FBool(True, 'bar')) is SBool(False)
        assert snot(FBool(True, 'foo') ^ SBool(True)) is SBool(True)
