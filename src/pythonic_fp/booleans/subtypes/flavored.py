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


"""Flavored Booleans."""

import threading
from collections.abc import Hashable
from typing import ClassVar, TypeVar, final
from ..subtypable import SBool

__all__ = ['FBool', 'truthy', 'falsy']

I = TypeVar('I', bound=int)


@final
class FBool(SBool):
    """Flavored Booleans.

    When you need to deal with different flavors of the truth.
    Each "flavor" is indexed by a hashable value.

    This type can also do (non-shortcut) Boolean logic using Python
    bitwise operators.

    """

    _truthy: 'ClassVar[dict[Hashable, FBool]]' = {}
    _truthy_lock: ClassVar[threading.Lock] = threading.Lock()

    _falsy: 'ClassVar[dict[Hashable, FBool]]' = {}
    _falsy_lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(
        cls, witness: object, flavor: Hashable
    ) -> 'FBool':
        """
        :param witness: determines truthiness of the ``FBool`` instance returned
        :param flavor: the ``flavor`` of ``FBool`` to created
        :returns: The truthy or falsy ``FBool`` instance of a particular ``flavor``

        """
        if witness:
            if flavor not in cls._truthy:
                with cls._truthy_lock:
                    if flavor not in cls._truthy:
                        cls._truthy[flavor] = super(SBool, cls).__new__(cls, True)
            return cls._truthy[flavor]
        else:
            if flavor not in cls._falsy:
                with cls._falsy_lock:
                    if flavor not in cls._falsy:
                        cls._falsy[flavor] = super(SBool, cls).__new__(cls, False)
            return cls._falsy[flavor]

    def __init__(self, witness: object, flavor: Hashable) -> None:
        self._flavor = flavor

    # override in derived classes
    def __repr__(self) -> str:
        if self:
            return f'FBool(True, {repr(self._flavor)})'
        return f'FBool(False, {repr(self._flavor)})'

    def __invert__(self) -> 'FBool':
        if self:
            return FBool(False, self._flavor)
        return FBool(True, self._flavor)

    def __and__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if self._flavor == other._flavor:
                return FBool(self and other, self._flavor)
        return SBool(self and other)

    def __rand__(self, other: I) -> SBool:
        return self & other

    def __or__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if self._flavor == other._flavor:
                return FBool(self or other, self._flavor)
        return SBool(self or other)

    def __ror__(self, other: I) -> SBool:
        return self | other

    def __xor__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if self._flavor == other._flavor:
                return FBool(not (self and other) and (self or other), self._flavor)
        return SBool(not (self and other) and (self or other))

    def __rxor__(self, other: I) -> SBool:
        return self ^ other

    def flavor(self) -> Hashable:
        """
        :returns: the flavor of the FBool

        """
        return self._flavor


def truthy(flavor: Hashable) -> FBool:
    """Get the truthy ``FBool`` of a particular ``flavor``.

    :param flavor: hashable value to determine which singleton ``flavor`` to return
    :returns: the truthy singleton of a particular  ``flavor``

    """
    return FBool(True, flavor)



def falsy(flavor: Hashable) -> FBool:
    """Get the falsy ``FBool`` of a particular ``flavor``.

    :param flavor: hashable value to determine which singleton ``flavor`` to return
    :returns: the falsy singleton of a particular  ``flavor``

    """
    return FBool(False, flavor)
