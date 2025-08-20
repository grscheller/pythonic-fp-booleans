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
from typing import ClassVar, Hashable, TypeVar
from ..subtypable import SBool

__all__ = [
    'FBool',
    'truthy',
    'falsy',
]

H = TypeVar('H', bound=Hashable)
I = TypeVar('I', bound=int)


class FBool(SBool):
    """Flavored Booleans.

    When you need to deal with different flavors of the truth.
    Each "flavor" corresponds to a hashable value.

    This type can also do (non-shortcut) Boolean logic using

    +------------+--------+------------+-------------+
    | Boolean op | symbol | dunder     | Python name |
    +============+========+============+=============+
    | and        | ``&``  | __and__    | bitwise and |
    +------------+--------+------------+-------------+
    | or         | ``|``  | __or__     | bitwise or  |
    +------------+--------+------------+-------------+
    | xor        | ``^``  | __xor__    | bitwise xor |
    +------------+--------+------------+-------------+
    | not        | ``~``  | __invert__ | bitwise not |
    +------------+--------+------------+-------------+

    .. warning::

       These "bitwise" operators could raise ``TypeError`` exceptions
       when applied against an ``FBool`` and objects not descended
       from ``FBool``.

    """

    _truthy: 'ClassVar[dict[Hashable, FBool]]' = {}
    _truthy_lock: ClassVar[threading.Lock] = threading.Lock()

    _falsy: 'ClassVar[dict[Hashable, FBool]]' = {}
    _falsy_lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, flavor: H, witness: object) -> 'FBool':
        """
        :param flavor: the ``flavor`` of ``FBool`` created.
        :param witness: the truthiness of ``witness`` determines truthiness of ``FBool`` returned
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

    def __init__(self, flavor: H, witness: object) -> None:
        if not hasattr(self, '_flavor'):
            self._flavor = flavor

    # override in derived classes
    def __repr__(self) -> str:
        if self:
            return f'FBool({repr(self._flavor)}, True)'
        return f'FBool({repr(self._flavor)}, False)'

    def __invert__(self) -> 'FBool':
        if self:
            return FBool(self._flavor, False)
        return FBool(self._flavor, True)

    def __and__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if isinstance(self._flavor, type(other._flavor)):
                if self and other:
                    return FBool(other._flavor, True)
                return FBool(other._flavor, False)
            if isinstance(other._flavor, type(self._flavor)):
                if self and other:
                    return FBool(self._flavor, True)
                return FBool(self._flavor, False)
            return SBool(other)
        return self & SBool(other)

    def __rand__(self, other: I) -> SBool:
        return self & other

    def __or__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if isinstance(self._flavor, type(other._flavor)):
                if self or other:
                    return FBool(other._flavor, True)
                return FBool(other._flavor, False)
            if isinstance(other._flavor, type(self._flavor)):
                if self or other:
                    return FBool(self._flavor, True)
                return FBool(self._flavor, False)
        return self | SBool(other)

    def __ror__(self, other: I) -> SBool:
        return self | other

    def __xor__(self, other: I) -> SBool:
        if isinstance(other, FBool):
            if isinstance(self._flavor, type(other._flavor)):
                if (self or other) and not (self and other):
                    return FBool(other._flavor, True)
                return FBool(other._flavor, False)
            if isinstance(other._flavor, type(self._flavor)):
                if self or other:
                    return FBool(self._flavor, True)
                return FBool(self._flavor, False)
        return self | SBool(other)

    def __rxor__(self, other: I) -> SBool:
        return self ^ other


def truthy(flavor: H) -> FBool:
    """ Get the truthy ``FBool`` of a particular ``flavor``.

    :param flavor: hashable value to determine which ``flavor`` of singleton to return
    :returns: the singleton with a particular  ``flavor``

    """
    return FBool(flavor, True)

def falsy(flavor: H) -> FBool:
    """ Get the falsy ``FBool`` of a particular ``flavor``.

    :param flavor: hashable value to determine which ``flavor`` of singleton to return
    :returns: the ``FBool`` singleton with a particular  ``flavor``

    """
    return FBool(flavor, False)
