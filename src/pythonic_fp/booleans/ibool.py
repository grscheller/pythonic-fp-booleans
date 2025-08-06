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


"""Subclassable Booleans

This class's sub-types represent different "flavors" of "truth" based
on a hashable value. Each flavor has one unique "truthy" and one unique
"falsy" instances.

The ``Truth(truth: H)`` and ``Lie(lie: H)`` subclass constructors
produce singletons based on their input parameter. When using type
hints, declare variables of these types as type ``SBool``.

.. note::
    
    Python does not permit bool to be subclassed, but ``int`` can
    be. Under-the-hood a ``bool`` is just an ``int``. This class
    inherits from ``int`` and relies on the underlying truthiness
    and falsiness of ``1`` and ``0``.

Best practices when used with these subclasses are:

- use `==` or `!=` for pure Boolean comparisons
- use `is` or `not is` if the type of truth matters
- only use ``SBool`` as a type, never as a constructor
- when using Python shortcut logic remember

  - an instance of ``Truth`` is truthy
  - an instance of ``Lie`` is falsy
  - shortcut logic is lazy

    - the last truthy thing evaluated is returned
    - and not converts it to a ``bool``

  - the `not` statement converts a ``BBool" or ``SBool" to an actual ``bool``

"""
from typing import Final, Hashable, TypeVar

__all__ = ['SBool', 'Truth', 'Lie', 'TRUTH', 'LIE']

H = TypeVar("H", bound=Hashable)


class IBool(int):
    """Better Boolean.

i   Like Python's built in bool, BBool is a subclass of int. Unlike bool,
    this version can be further subclassed. It can be used with Python
    `and` and `or` short-cut logic. The ``not`` operator will just return
    a ``bool``. Use the ``bnot`` function to return a ``BBool``.

    """

    def __new__(cls, val: int) -> 'BBool':
        val = 1 if val else 0
        return super(SBool, cls).__new__(cls, val)

    def __repr__(self) -> str:
        if self:
            return 'IBool(1)'
        return 'IBool(0)'

    def __str__(self) -> str:
        if self:
            return 'IBTrue'
        return 'IBFalse'

    def __add__(self, other):
        if issubclass(type(other), int):
            if self or other:
                return BBool(1)
            return BBool(0)
        msg = f"unsupported operand type(s) for +: 'BBool' and '{type(other)}'"
        raise TypeError(msg)

    def __radd__(self, other):
        if issubclass(type(other), int):
            if self or other:
                return BBool(1)
            return BBool(0)
        msg = f"unsupported operand type(s) for +: '{type(other)}' and 'BBool'"
        raise TypeError(msg)

    def __mult__(self, other):
        if issubclass(type(other), int):
            if self and other:
                return BBool(1)
            return BBool(0)
        msg = f"unsupported operand type(s) for +: 'BBool' and '{type(other)}'"
        raise TypeError(msg)

    def __rmult__(self, other):
        if issubclass(type(other), int):
            if self and other:
                return BBool(1)
            return BBool(0)
        msg = f"unsupported operand type(s) for +: '{type(other)}' and 'BBool'"
        raise TypeError(msg)


def bnot(bbool: BBool) -> BBool:
    """Return the BBool of the opposite truthiness.

    .. note::

        Trying to use the Python ``not`` operator for this will just
        return a ``bool``. There is no ``__not__`` dunder method
        that will change the behavior of ``not``.

    """
    if bbool:
        return BBool(0)
    return BBool(1)


class SBool[H](IBool):
    """
    .. important::

        Only use SBool as a type, never as a constructor. Use its

    """
    _instances: 'dict[str, Truth]' = dict()

    def __new__(cls, flavor: H) -> 'Truth':
        if flavor not in cls._instances:
            cls._instances[flavor] = super(SBool, cls).__new__(cls, 1)
        return cls._instances[flavor]

    def __new__(cls) -> 'SBool':
        return super(SBool, cls).__new__(cls, 0)

    def __repr__(self) -> str:
        if self:
            return 'SBool(1)'
        return 'SBool(0)'

    def flavor(self) -> str:
        raise NotImplementedError


class Truth[H](SBool[H]):
    """Truthy singleton SBool subclass.

    .. note::
        When using type hints, declare variables SBool, not Truth.

    """

    _instances: 'dict[str, Truth]' = dict()

    def __new__(cls, flavor: str = 'DEFAULT_TRUTH') -> 'Truth':
        if flavor not in cls._instances:
            cls._instances[flavor] = super(SBool, cls).__new__(cls, 1)
        return cls._instances[flavor]

    def __init__(self, flavor: str = 'DEFAULT_TRUTH') -> None:
        self._flavor = flavor

    def __repr__(self) -> str:
        return f"Truth('{self._flavor}')"

    def flavor(self) -> str:
        return self._flavor


class Lie[H](SBool[H]):
    """Falsy singleton SBool subclass.

    .. note::
        When using type hints, declare variables SBool, not Lie.

    """

    _instances: 'dict[str, Lie]' = dict()

    def __new__(cls, flavor: H = '') -> 'Lie':
        if flavor not in cls._instances:
            cls._instances[flavor] = super(SBool, cls).__new__(cls, 0)
        return cls._instances[flavor]

    def __init__(self, flavor: str = '') -> None:
        self._flavor = flavor

    def __repr__(self) -> str:
        return f"Lie('{self._flavor}')"

    def flavor(self) -> str:
        return self._flavor


TRUTH: Final[Truth] = Truth()
LIE: Final[Lie] = Lie()


def snot(val: SBool) -> SBool:
    """Return the opposite truthiness of the same flavor of truth.

    .. note::

        Trying to use the Python ``not`` operator for this will just
        return a ``bool``. There is no ``__not__`` dunder method
        that will change the behavior of ``not``.

    """
    if val:
        return Lie(val.flavor())
    return Truth(val.flavor())
