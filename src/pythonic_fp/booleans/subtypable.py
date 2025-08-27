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


"""Subtypable Booleans."""

import threading
from collections.abc import Hashable
from typing import cast, ClassVar, Final, Never, overload
from pythonic_fp.gadgets.lca import latest_common_ancestor
from pythonic_fp.sentinels.novalue import NoValue

__all__ = [
    'SBool',
    'snot',
    'TRUTH',
    'LIE',
]

_novalue = NoValue()


class SBool(int):
    """Subtypable Booleans.

    Like Python's built in bool, class SBool is a subclass of int.
    Unlike bool, this version can be further subclassed. It can be
    used with Python ``and`` and ``or`` short-cut logic. The ``not``
    operator will just return a ``bool``. Use the ``snot`` function
    to return an ``SBool`` or ``SBool`` subclass.

    This type and its subtypes can also do (non-shortcut) Boolean logic
    using Python bitwise operators.
    """
    _falsy: 'ClassVar[SBool | NoValue]' = _novalue
    _falsy_lock: ClassVar[threading.Lock] = threading.Lock()

    _truthy: 'ClassVar[SBool | NoValue]' = _novalue
    _truthy_lock: ClassVar[threading.Lock] = threading.Lock()

    @overload
    def __new__(cls) -> 'SBool': ...
    @overload
    def __new__(cls, witness: object) -> 'SBool': ...

    def __new__(cls, witness: object = False, flavor: Hashable = _novalue) -> 'SBool':
        """
        :param witness: Determines truthiness of the ``SBool``.
        :returns: The truthy or falsy SBool class instance.
        """
        if witness:
            if cls._truthy is _novalue:
                with cls._truthy_lock:
                    if cls._truthy is _novalue:
                        cls._truthy = super().__new__(cls, 1)
            return cast(SBool, cls._truthy)
        else:
            if cls._falsy is _novalue:
                with cls._falsy_lock:
                    if cls._falsy is _novalue:
                        cls._falsy = super().__new__(cls, 0)
            return cast(SBool, cls._falsy)

    def __init__(self, witness: object = False, flavor: Hashable = _novalue) -> None:
        self._flavor = flavor

    # override in derived classes
    def __repr__(self) -> str:
        if self:
            return 'TRUTH'
        return 'LIE'

    def __invert__(self) -> 'SBool':
        if self:
            return type(self)(False)
        return type(self)(True)

    def __and__(self, other: int) -> 'SBool | Never':
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = (
                f"unsupported operand type(s) for &: '{type(self)}' and '{type(other)}'"
            )
            raise TypeError(msg)

        if self and other:
            return SBool(base_class(1))
        return SBool(base_class(0))

    def __rand__(self, other: int) -> 'SBool | Never':
        return self.__and__(other)

    def __or__(self, other: int) -> 'SBool | Never':
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = (
                f"unsupported operand type(s) for |: '{type(self)}' and '{type(other)}'"
            )
            raise TypeError(msg)

        if self or other:
            return SBool(base_class(1))
        return SBool(base_class(0))

    def __ror__(self, other: int) -> 'SBool | Never':
        return self.__and__(other)

    def __xor__(self, other: int) -> 'SBool | Never':
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = (
                f"unsupported operand type(s) for ^: '{type(self)}' and '{type(other)}'"
            )
            raise TypeError(msg)

        if self and not other or other and not self:
            return SBool(base_class(1))
        return SBool(base_class(0))

    def __rxor__(self, other: int) -> 'SBool | Never':
        return self.__and__(other)


def snot(sbool: SBool) -> SBool:
    """Return the ``SBool`` subtype of the opposite truthiness.

    .. note::

        Trying to use the Python ``not`` operator for this will just
        return a ``bool``. There is no ``__not__`` dunder method
        that will change the behavior of ``not``.

    :param sbool: An ``SBool`` or ``SBool`` subtype.
    :returns: The ``SBool`` or ``SBool`` subtype of the opposite truthiness.
    """
    return ~sbool


TRUTH: Final[SBool] = SBool(True)  #: The truthy singleton of type ``SBool``.
LIE: Final[SBool] = SBool(False)  #: The falsy singleton of type ``SBool``.
