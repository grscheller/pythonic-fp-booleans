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
from typing import cast, ClassVar, Final, Self
from pythonic_fp.gadgets.sentinels.novalue import NoValue
from .subtypable import SBool

__all__ = [
    'TF_Bool',
    'T_Bool',
    'F_Bool',
    'ALWAYS',
    'NEVER',
]

_novalue = NoValue()


class TF_Bool(SBool):
    """
    .. admonition:: Truthy-Falsy Booleans

        A Boolean implementation whose distinct truthy and falsy
        values are distinct singleton subclasses, not just
        distinct singleton values.

        A subtype of ``SBool``.

        .. tip::

            Logically combine these using Python's bitwise operators.

        .. warning::

            Although these datastructures are completely compatible
            with Python shortcut evaluation, care needs to be taken when
            using them with the ``and``, ``or``, and ``not`` builtins.

            For example, ``~ALWAYS is NEVER`` but ``not ALWAYS is False``
            because ``ALWAYS`` is truthy.

            Similarly, ``(ALWAYS and False) is False`` while
            ``(ALWAYS or False) is ALWAYS``.

    """

    def __new__(cls, witness: object, flavor: Hashable = NoValue()) -> Self:
        """
        .. admonition:: new

            :param witness: Determines which subtype, ``T_Bool`` or ``F_Bool`` to return.
            :param flavor: Ignored parameter, only two flavors, one truthy and one falsy.
            :returns: The singleton truthy or singleton falsy instances.

        """
        if witness:
            return cast(Self, T_Bool())
        return cast(Self, F_Bool())

    def __invert__(self) -> TF_Bool:
        if self:
            return F_Bool()
        return T_Bool()

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            - if truthy return 'TF_Bool(True)'
            - if falsy return 'TF_Bool(False)'

            :returns: A string to reproduce the ``TF_Bool``.

        """
        if self:
            return 'TF_Bool(True)'
        return 'TF_Bool(False)'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            - if truthy return 'ALWAYS'
            - if falsy return 'NEVER'

            :returns: A string meaningful to an end user.

        """
        if self:
            return 'ALWAYS'
        return 'NEVER'


class T_Bool(TF_Bool):
    """
    .. admonition:: Truthy TF_Bool subclass

         Type of the truthy singleton ``TS_Bool`` instance.
         A distinct type from ``F_Bool``.

    """
    _truthy: 'ClassVar[T_Bool | NoValue]' = _novalue
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, witness: object = _novalue, flavor: Hashable | NoValue = _novalue) -> Self:
        """
        .. admonition:: new

            :param witness: Ignored parameter, a T_Bool is always truthy.
            :param flavor: Ignored parameter, only one truthy "flavor".
            :returns: The truthy ``T_Bool`` singleton instance.

        """
        if cls._truthy is _novalue:
            with cls._lock:
                if cls._truthy is _novalue:
                    cls._truthy = super(SBool, cls).__new__(cls, 1)
        return cast(Self, cls._truthy)

    def __and__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return other
        return other.__and__(self)

    def __or__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return self
        return other.__or__(self)

    def __xor__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            if other:
                return ~self
            return self
        return other.__xor__(self)

    def __rand__(self, other: int) -> int:
        return self | other

    def __ror__(self, other: int) -> int:
        return self | other

    def __rxor__(self, other: int) -> int:
        return self ^ other


class F_Bool(TF_Bool):
    """
    .. admonition:: Falsy TF_Bool subclass

         Type of the falsy singleton ``TS_Bool`` instance.
         A distinct type from ``T_Bool``.

    """
    _falsy: 'ClassVar[F_Bool | NoValue]' = _novalue
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, witness: object = _novalue, flavor: Hashable | NoValue = _novalue) -> Self:
        """
        .. admonition:: new

            :param witness: Parameter ignored, an ``F_Bool`` is always falsy.
            :param flavor: Parameter ignored, only one falsy "flavor".
            :returns: The falsy ``F_Bool`` singleton instance.

        """
        if cls._falsy is _novalue:
            with cls._lock:
                if cls._falsy is _novalue:
                    cls._falsy = super(SBool, cls).__new__(cls, 0)
        return cast(Self, cls._falsy)

    def __and__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return self
        return super().__and__(other)

    def __or__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return other
        return super().__and__(other)

    def __xor__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            if other:
                return other
            return self
        return super().__and__(other)

    def __rand__(self, other: int) -> int:
        return self | other

    def __ror__(self, other: int) -> int:
        return self | other

    def __rxor__(self, other: int) -> int:
        return self ^ other


ALWAYS: Final[TF_Bool] = T_Bool()
"""
.. admonition:: ALWAYS

    :var ALWAYS: The truthy singleton ``TF_Bool`` subtyped instance.

"""

NEVER: Final[TF_Bool] = F_Bool()
"""
.. admonition:: Never

    :var NEVER: The falsy singleton ``TF_Bool`` subtyped instance.

"""
