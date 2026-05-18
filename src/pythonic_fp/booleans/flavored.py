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
from collections.abc import Hashable
from typing import ClassVar, final, Self
from .subtypable import SBool

__all__ = ['FBool', 'truthy', 'falsy']


@final
class FBool(SBool):
    """
    .. admonition:: Favored Booleans

        When different flavors of the truth matter. Each ``FBool`` is
        an ``SBool`` subtype corresponding to a hashable ``flavor``.

        .. warning::

            Combining FBool instances of different flavors with
            bitwise operators will result in a runtime ValueError
            exception.

    """

    _falsy_dict: 'ClassVar[dict[Hashable, FBool]]' = {}
    _falsy_dict_lock: ClassVar[threading.Lock] = threading.Lock()

    _truthy_dict: 'ClassVar[dict[Hashable, FBool]]' = {}
    _truthy_dict_lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, witness: object, flavor: Hashable) -> Self:
        """
        .. admonition:: new

            Traditional singleton pattern but with a ClassVar dict
            to store the for truthy or falsy singleton for each
            hashable flavor.

            :param witness: Determines truthiness of the ``FBool`` instance returned.
            :param flavor: The ``flavor`` of ``FBool`` to created.
            :returns: The truthy or falsy ``FBool`` instance of a particular ``flavor``.

        """
        if witness:
            if flavor not in cls._truthy_dict:
                with cls._truthy_dict_lock:
                    if flavor not in cls._truthy_dict:
                        cls._truthy_dict[flavor] = super(SBool, cls).__new__(cls, 1)
            return cls._truthy_dict[flavor]
        else:
            if flavor not in cls._falsy_dict:
                with cls._falsy_dict_lock:
                    if flavor not in cls._falsy_dict:
                        cls._falsy_dict[flavor] = super(SBool, cls).__new__(cls, 0)
            return cls._falsy_dict[flavor]

    def __init__(self, witness: object, flavor: Hashable) -> None:
        """
        .. admonition:: initialize

            Let the flavored boolean know its flavor.

            :param witness: Determines truthiness of the ``FBool`` instance returned.
            :param flavor: The ``flavor`` of ``FBool`` to created.
            :type flavor: ``H: Hashable``
            :returns: The truthy or falsy ``FBool`` instance of a particular ``flavor``.
            :raises ValueError: If different flavors compared with bitwise operators.

        """
        if not hasattr(self, '_flavor'):
            self._flavor = flavor

    def __and__(self, other: int) -> int:
        if type(other) is type(self):
            if other.flavor() != self._flavor:
                msg = 'Error: diffent flavored booleans compared with & operator'
                raise ValueError(msg)
            if self and other:
                return FBool(1, self._flavor)
            else:
                return FBool(0, self._flavor)
        return super().__and__(other)

    def __or__(self, other: int) -> int:
        if type(other) is type(self):
            if other.flavor() != self.flavor():
                msg = 'Error: diffent flavored booleans compared with | operator'
                raise ValueError(msg)
            if self or other:
                return FBool(1, self._flavor)
            else:
                return FBool(0, self._flavor)
        return super().__or__(other)

    def __xor__(self, other: int) -> int:
        if type(other) is type(self):
            if other.flavor() != self._flavor:
                msg = 'Error: diffent flavored booleans compared with ^ operator'
                raise ValueError(msg)
            if (self or other) and not (self and other):
                return FBool(1, self._flavor)
            else:
                return FBool(0, self._flavor)
        return super().__xor__(other)

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Create strings of the form

            - `FBool(True, repr_flavor)'
            - `FBool(False, repr_flavor)'

            Where repr_flavor = repr(self.flavor())

            :returns: A String to reproduce the flavored boolean.

        """
        if self:
            return f'FBool(True, {repr(self._flavor)})'
        return f'FBool(False, {repr(self._flavor)})'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Create strings of the form

            - `FBool(True, str_flavor)'
            - `FBool(False, str_flavor)'

            Where str_flavor = str(self.flavor())

            :returns: A String to meaningful to an end user.

        """
        if self:
            return f'FBool(True, {str(self._flavor)})'
        return f'FBool(False, {str(self._flavor)})'

    def flavor(self) -> Hashable:
        """
        .. admonition:: flavor

            Get the ``flavor`` of the ``FBool``, a hashable value.

            :returns: The ``flavor``.

        """
        return self._flavor


def truthy(flavor: Hashable) -> FBool:
    """
    .. admonition:: function truthy

        Returns the truthy singleton ``FBool`` of a particular ``flavor``.

        :param flavor: Hashable value to determine which
                       singleton ``flavor`` to return.
        :returns: The truthy singleton of a particular ``flavor``.

    """
    return FBool(True, flavor)


def falsy(flavor: Hashable) -> FBool:
    """
    .. admonition:: Function falsy

        Returns the falsy singleton ``FBool`` of a particular ``flavor``.

        :param flavor: Hashable value to determine which
                       singleton ``flavor`` to return.
        :returns: The falsy singleton of a particular ``flavor``.

    """
    return FBool(False, flavor)
