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

import threading
from typing import ClassVar, Hashable, TypeVar
from subtypable_boolean import SBool

__all__ = [
    'FBool',
    'truthy',
    'falsy',
]

H = TypeVar('H', bound=Hashable)
I = TypeVar('I', bound=int)

class FBool(SBool):
    _truthy: ClassVar[dict[Hashable, FBool]]
    _truthy_lock: ClassVar[threading.Lock]

    _falsy: ClassVar[dict[Hashable, FBool]]
    _falsy_lock: ClassVar[threading.Lock]

    def __new__(cls, flavor: H, witness: object) -> FBool: ...
    def __init__(self, flavor: H, witness: object) -> None: ...
    def __repr__(self) -> str: ...
    def __invert__(self) -> 'FBool': ...
    def __and__(self, other: I) -> SBool: ...
    def __rand__(self, other: I) -> SBool: ...
    def __or__(self, other: I) -> SBool: ...
    def __ror__(self, other: I) -> SBool: ...
    def __xor__(self, other: I) -> SBool: ...
    def __rxor__(self, other: I) -> SBool: ...

def truthy(flavor: H) -> FBool: ...
def falsy(flavor: H) -> FBool: ...
