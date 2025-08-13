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

from typing import ClassVar, Final, final, Never, Self, TypeVar

__all__ = ['SBool', 'snot', 'TRUTH', 'LIE']

I = TypeVar('I', bound=int)

class SBool(int):
    _instance0: ClassVar[SBool | None]
    _instance1: ClassVar[SBool | None]
    def __new__(cls, obj: object) -> SBool: ...
    def __repr__(self) -> str: ...
    @final
    def __invert__(self) -> Self: ...
    @final
    def __and__(self, other: I) -> Self | Never: ...
    @final
    def __rand__(self, other: I) -> Self | Never: ...
    @final
    def __or__(self, other: I) -> Self | Never: ...
    @final
    def __ror__(self, other: I) -> Self | Never:
        return self.__and__(other)
    @final
    def __xor__(self, other: I) -> Self | Never: ...
    @final
    def __rxor__(self, other: I) -> Self | Never: ...

S = TypeVar('S', bound=SBool)

def snot(sbool: S) -> S: ...

TRUTH: Final[SBool] = SBool(True)
LIE: Final[SBool] = SBool(False)
