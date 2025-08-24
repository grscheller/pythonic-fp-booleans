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


"""Booleans whose "truthy" and "falsy" instances are distinct subtypes."""

import threading
from collections.abc import Hashable
from typing import cast, ClassVar, Final, final, TypeVar
from pythonic_fp.sentinels.novalue import NoValue
from ..subtypable import SBool

__all__ = [
    'TF_Boolean',
    'TF_Bool',
    'T_Bool',
    'F_Bool',
    'ALWAYS',
    'NEVER_EVER',
]

_novalue = NoValue()

I = TypeVar('I', bound=int)


class TF_Bool(SBool):
    """Subclass of ``SBool`` whose truthy values and falsy values are
    different singleton subtypes.

    This type can also do (non-shortcut) Boolean logic using Python
    bitwise operators.

    """

    def __new__(cls, witness: object, flavor: Hashable = NoValue()) -> 'TF_Bool':
        """

        :param witness: determines which subtype, ``T_Bool`` or ``F_Bool`` is returned
        :param flavor: ignored parameter, only two flavors, one truthy and one falsy
        :returns: either the singleton truthy or singleton falsy subtypes

        """
        if witness:
            return T_Bool()
        return F_Bool()

    def __repr__(self) -> str:
        if self:
            return 'ALWAYS'
        return 'NEVER_EVER'

    def __invert__(self) -> 'TF_Bool':
        if self:
            return F_Bool()
        return T_Bool()

    def __and__(self, other: I) -> 'TF_Bool':
        if self and other:
            return T_Bool()
        return F_Bool()

    def __rand__(self, other: I) -> 'TF_Bool':
        return self.__and__(other)

    def __or__(self, other: I) -> 'TF_Bool':
        if self or other:
            return T_Bool()
        return F_Bool()

    def __ror(self, other: I) -> 'TF_Bool':
        return self.__or__(other)

    def __xor__(self, other: I) -> 'TF_Bool':
        if self and not other or other and not self:
            return T_Bool()
        return F_Bool()

    def __rxor(self, other: I) -> 'TF_Bool':
        return self.__xor__(other)


@final
class T_Bool(TF_Bool):
    """The subtype of ``TF_Bool`` which is always Truthy."""

    _truthy: 'ClassVar[T_Bool | NoValue]' = _novalue
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(
        cls, witness: object = _novalue, flavor: Hashable = _novalue
    ) -> 'T_Bool':
        """

        :param witness: ignored parameter, a T_Bool is always truthy
        :param flavor: ignored parameter, only one truthy "flavor"
        :returns: the truthy ``T_Bool`` singleton instance

        """
        if cls._truthy is _novalue:
            with cls._lock:
                if cls._truthy is _novalue:
                    cls._truthy = super(SBool, cls).__new__(cls, True)
        return cast(T_Bool, cls._truthy)

    def __repr__(self) -> str:
        return 'ALWAYS'


@final
class F_Bool(TF_Bool):
    """The subtype of ``TF_Bool`` which is always Falsy."""

    _falsy: 'ClassVar[F_Bool | NoValue]' = _novalue
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, witness: object = _novalue, flavor: Hashable = _novalue) -> 'F_Bool':
        """

        :param witness: parameter ignored, an ``F_Bool`` is always falsy
        :param flavor: parameter ignored, only one falsy "flavor"
        :returns: the falsy ``F_Bool`` singleton instance

        """
        if cls._falsy is _novalue:
            with cls._lock:
                if cls._falsy is _novalue:
                    cls._falsy = super(SBool, cls).__new__(cls, False)
        return cast(F_Bool, cls._falsy)

    def __repr__(self) -> str:
        return 'NEVER_EVER'

TF_Boolean = T_Bool | F_Bool | TF_Bool  #: use only as a type, never a constructor

ALWAYS: Final[TF_Boolean] = T_Bool()  #: the truthy singleton ``TF_Bool`` subtype
NEVER_EVER: Final[TF_Boolean] = F_Bool()  #: the falsy singleton ``TF_Bool`` subtype
