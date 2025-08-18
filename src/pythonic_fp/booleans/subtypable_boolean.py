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
from typing import ClassVar, Final, Never, TypeVar
from pythonic_fp.gadgets.lca import latest_common_ancestor

__all__ = [
    'SBool',
    'snot',
    'TRUTH',
    'LIE',
]

I = TypeVar('I', bound=int)


class SBool(int):
    """Subtypable Booleans.

    Like Python's built in bool, class SBool is a subclass of int.
    Unlike bool, this version can be further subclassed. It can be
    used with Python ``and`` and ``or`` short-cut logic. The ``not``
    operator will just return a ``bool``. Use the ``snot`` function
    to return an ``SBool`` or ``SBool`` subclass.

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
       when applied against an ``SBool`` and objects not descended
       from ``SBool``.

    """

    _falsy_: 'ClassVar[SBool | None]' = None
    _falsy_lock: ClassVar[threading.Lock] = threading.Lock()

    _truthy_: 'ClassVar[SBool | None]' = None
    _truthy_lock: ClassVar[threading.Lock] = threading.Lock()

    # will need to make thread safe when subclassed instances brought in
    def __new__(cls, witness: object) -> 'SBool':
        """
        :param value: The truthiness of obj determines truthiness of SBool created.
        :returns: The truthy or falsy SBool subclass instance.

        """
        if witness:
            if cls._truthy_ is None:
                with cls._truthy_lock:
                    if cls._truthy_ is None:
                        cls._truthy_ = super().__new__(cls, 1)
            return cls._truthy_
        else:
            if cls._falsy_ is None:
                with cls._falsy_lock:
                    if cls._falsy_ is None:
                        cls._falsy_ = super().__new__(cls, 0)
            return cls._falsy_

    # override in derived classes
    def __repr__(self) -> str:
        if self:
            return 'TRUTH'
        return 'LIE'

    def __invert__(self) -> 'SBool':
        if self:
            return type(self)(False)
        return type(self)(True)

    def __and__(self, other: I) -> 'SBool | Never':
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

    def __rand__(self, other: I) -> 'SBool | Never':
        return self.__and__(other)

    def __or__(self, other: I) -> 'SBool | Never':
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

    def __ror__(self, other: I) -> 'SBool | Never':
        return self.__and__(other)

    def __xor__(self, other: I) -> 'SBool | Never':
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

    def __rxor__(self, other: I) -> 'SBool | Never':
        return self.__and__(other)


S = TypeVar('S', bound=SBool)


def snot(sbool: S) -> S:
    """Return the subtype ``S`` of ``SBool`` of the opposite truthiness.

    .. note::

        Trying to use the Python ``not`` operator for this will just
        return a ``bool``. There is no ``__not__`` dunder method
        that will change the behavior of ``not``.

    """
    if sbool:
        return type(sbool)(False)
    return type(sbool)(True)


TRUTH: Final[SBool] = SBool(True)
LIE: Final[SBool] = SBool(False)
