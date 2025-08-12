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

from typing import Final, final, Never, Self, TypeVar

__all__ = ['SBool', 'snot', 'TRUTH', 'LIE']

I = TypeVar('I', bound=int)

class SBool(int):
    def __new__(cls, value: int) -> Self: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @final
    def __neg__(self) -> Self: ...
    @final
    def __add__(self, other: I) -> Self | Never: ...
    @final
    def __radd__(self, other: I) -> Self | Never: ...
    @final
    def __mul__(self, other: I) -> Self | Never: ...
    @final
    def __rmul__(self, other: I) -> Self | Never: ...

S = TypeVar('S', bound=SBool)

def snot(sbool: S) -> S: ...

TRUTH: Final[SBool] = SBool(1)
LIE: Final[SBool] = SBool(0)
