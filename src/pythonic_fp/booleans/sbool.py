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

from typing import cast, ClassVar, Final, final, Never, Self, TypeVar
from pythonic_fp.gadgets.lca import latest_common_ancestor

__all__ = ['SBool', 'snot', 'TRUTH', 'LIE']

I = TypeVar('I', bound=int)

# IDEA: provide a Final classmethod that generates the subclasses?
# The cls.__bases__ can provide immediate predecessor classes.
class SBool(int):
    """Subtypable Booleans.

    Like Python's built in bool, class SBool is a subclass of int.
    Unlike bool, this version can be further subclassed. It can be
    used with Python ``and`` and ``or`` short-cut logic. The ``not``
    operator will just return a ``bool``. Use the ``snot`` function
    to return an ``SBool`` or one of its subclasses.

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

       These "bitwise" operators will raise ``TypeError`` exceptions
       when applied against an ``SBool`` and objects not descended
       from ``SBool``.

    """
    # will need to replace with a dictionary for subclass instances?
    # or require such variables in each subclass?
    _instance0: 'ClassVar[SBool | None]' = None
    _instance1: 'ClassVar[SBool | None]' = None

    # will need to make thread safe when subclassed instances brought in
    def __new__(cls, obj: object) -> 'SBool':
        """
        :param value: The truthiness of obj determines truthiness of SBool created.
        :returns: The truthy or falsy SBool subclass instance

        """
        if obj:
            if cls._instance1 is None:
                cls._instance1 = super(SBool, cls).__new__(cls, 1)
            return cls._instance1
        else:
            if cls._instance0 is None:
                cls._instance0 = super(SBool, cls).__new__(cls, 0)
            return cls._instance0

    # override in derived classes
    def __repr__(self) -> str:
        if self:
            return 'TRUTH'
        return 'LIE'

    @final
    def __invert__(self) -> Self:
        if self:
            return type(self)(False)
        return type(self)(True)

    @final
    def __and__(self, other: I) -> Self | Never:
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = f"unsupported operand type(s) for &: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if base_class is int or base_class is object:
            msg = f"unsupported operand type(s) for &: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if self and other:
            return cast(Self, base_class(1))
        return cast(Self, base_class(0))

    @final
    def __rand__(self, other: I) -> Self | Never:
        return self.__and__(other)

    @final
    def __or__(self, other: I) -> Self | Never:
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = f"unsupported operand type(s) for |: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if base_class is int or base_class is object:
            msg = f"unsupported operand type(s) for |: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if self or other:
            return cast(Self, base_class(1))
        return cast(Self, base_class(0))

    @final
    def __ror__(self, other: I) -> Self | Never:
        return self.__and__(other)

    @final
    def __xor__(self, other: I) -> Self | Never:
        try:
            base_class = latest_common_ancestor(type(self), type(other))
        except TypeError:
            msg = f"unsupported operand type(s) for ^: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if base_class is int or base_class is object:
            msg = f"unsupported operand type(s) for ^: '{type(self)}' and '{type(other)}'"
            raise TypeError(msg)

        if self and not other or other and not self:
            return cast(Self, base_class(1))
        return cast(Self, base_class(0))

    @final
    def __rxor__(self, other: I) -> Self | Never:
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
        return type(sbool)(0)
    return type(sbool)(1)

# Optionally define other "truthy" and "falsy" types for subtypes.
TRUTH: Final[SBool] = SBool(True)
LIE: Final[SBool] = SBool(False)
