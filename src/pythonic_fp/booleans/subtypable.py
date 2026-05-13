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
from typing import cast, ClassVar, Final, overload, Self
from types import NotImplementedType
from pythonic_fp.gadgets import first_common_ancestor as fca
from pythonic_fp.gadgets.sentinels.novalue import NoValue

__all__ = ['SBool', 'TRUTH', 'LIE']


class SBool(int):
    """
    .. admonition:: Subtypable Boolean

        Like Python's built in bool, class ``SBool`` is a singleton subclass
        of int. Unlike bool, it can be further subclassed.

        ``SBool`` and its subtypes can also do (non-shortcut) Boolean logic
        using Python bitwise operators.

        +-------------------+--------+------------+
        | Boolean operation | symbol | dunder     |
        +===================+========+============+
        |       not         | ``~``  | __invert__ |
        +-------------------+--------+------------+
        |       and         | ``&``  | __and__    |
        +-------------------+--------+------------+
        |       or          | ``|``  | __or__     |
        +-------------------+--------+------------+
        |       xor         | ``^``  | __xor__    |
        +-------------------+--------+------------+

        While compatible with Python  short-cut logic, , the ``not``
        operator unfortunately always returns a ``bool``.

        .. tip::

            Use the bitwise ``~`` operator to return
            an opposite ``SBool`` instance or subclass instance.

        .. note::

            These operators are contravariant, that is they will return
            the instance of the latest common ancestor of their
            arguments. More specifically, the instance returned will
            have the type of the least upper bound in the inheritance
            graph of the classes of the two arguments.

            .. warning::

                The "bitwise" operators can raise ``TypeError``
                exceptions when applied against an ``SBool`` and
                objects not descended from ``int``.

    """

    _falsy: 'ClassVar[SBool | NoValue]' = NoValue()
    _falsy_lock: ClassVar[threading.Lock] = threading.Lock()

    _truthy: 'ClassVar[SBool | NoValue]' = NoValue()
    _truthy_lock: ClassVar[threading.Lock] = threading.Lock()

    @overload
    def __new__(cls, witness: object) -> Self: ...
    @overload
    def __new__(cls, witness: object, flavor: Hashable | NoValue = NoValue()) -> Self: ...

    def __new__(
        cls,
        witness: object,
        flavor: Hashable | NoValue = NoValue(),
    ) -> 'SBool':
        """
        .. admonition:: new

            :param witness: Determines truthiness of the ``SBool``.
            :param flavor: Ignored 
            :returns: The truthy or falsy SBool class instance.

        """
        novalue = NoValue()
        if witness:
            if cls._truthy is novalue:
                with cls._truthy_lock:
                    if cls._truthy is novalue:
                        cls._truthy = super().__new__(cls, 1)
            return cast(SBool, cls._truthy)
        else:
            if cls._falsy is novalue:
                with cls._falsy_lock:
                    if cls._falsy is novalue:
                        cls._falsy = super().__new__(cls, 0)
            return cast(SBool, cls._falsy)

    @overload
    def __init__(self, witness: object) -> None: ...
    @overload
    def __init__(self, witness: object, flavor: Hashable) -> None: ...

    def __init__(
        self,
        witness: object = False,
        flavor: Hashable | NoValue = NoValue(),
    ) -> None:
        """
        .. admonition:: init

            :param witness: Determines the truthiness of the ``SBool``.
            :param flavor: Ignored by ``SBool``,
                           for Liskov Substitution Principle.
        """
        self._flavor: Hashable | NoValue = NoValue()

    def __invert__(self) -> int:
        if self:
            return type(self)(False, self._flavor)
        return type(self)(True, self._flavor)

    def __and__(self, other: int) -> int:
        if not isinstance(other, type(self)):
            return NotImplemented

        try:
            base_class = fca(type(self), type(other))
        except TypeError:
            if type(other) is bool:
                base_class = int
            else:
                msg = f"unsupported operand type(s) for &: '{type(self)}' and '{type(other)}'"
                raise TypeError(msg)

        if issubclass(base_class, SBool):
            if self._flavor == other._flavor:
                flavor = self._flavor
            else:
                flavor = NoValue()

            if self and other:
                return base_class(True, flavor)
            return base_class(False, flavor)
        else:
            return int(self) & int(other)

    def __or__(self, other: int) -> int:
        try:
            base_class = fca(type(self), type(other))
        except TypeError:
            if type(other) is bool:
                base_class = int
            else:
                msg = f"unsupported operand type(s) for |: '{type(self)}' and '{type(other)}'"
                raise TypeError(msg)

        if issubclass(base_class, SBool):
            if self._flavor == cast(SBool, other)._flavor:
                flavor = self._flavor
            else:
                flavor = NoValue()

            if self or other:
                return base_class(True, flavor)
            return base_class(False, flavor)
        else:
            return int(self) | int(other)

    def __xor__(self, other: int) -> int:
        try:
            base_class = fca(type(self), type(other))
        except TypeError:
            if type(other) is bool:
                base_class = int
            else:
                msg = f"unsupported operand type(s) for ^: '{type(self)}' and '{type(other)}'"
                raise TypeError(msg)

        if issubclass(base_class, SBool):
            if self._flavor == cast(SBool, other)._flavor:
                flavor = self._flavor
            else:
                flavor = NoValue()

            if self and not other or other and not self:
                return base_class(True, flavor)
            return base_class(False, flavor)
        else:
            return int(self) ^ int(other)

    def __rand__(self, other: int) -> int:
        return self & other

    def __ror__(self, other: int) -> int:
        return self | other

    def __rxor__(self, other: int) -> int:
        return self ^ other

    # override in derived classes
    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            - 'SBool(True)' if truthy
            - 'SBool(False)' if falsy

            :returns: A string to reproduce the ``SBool``.

        """
        if self:
            return 'SBool(True)'
        return 'SBool(False)'

    # override in derived classes
    def __str__(self) -> str:
        """
        .. admonition:: user string

            - 'TRUTH' if truthy
            - 'LIE' if falsy

            :returns: A string meaningful to an end user.

        """
        if self:
            return 'TRUTH'
        return 'LIE'


TRUTH: Final[SBool] = SBool(True)
"""
.. admonition:: TRUTH

    :var TRUTH: The truthy singleton of type ``SBool``.

"""

LIE: Final[SBool] = SBool(False)
"""
.. admonition:: LIE

    :var LIE: The falsy singleton of type ``SBool``.

"""
