# Copyright 2023-2026 Geoffrey R. Scheller
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

from collections.abc import Hashable
from threading import Lock
from typing import ClassVar, Final, Self, cast, final

from .subtypable import SBool

__all__ = [
    'TF_Bool',
    'T_Bool',
    'F_Bool',
    'ALWAYS',
    'NEVER',
]


class TF_Bool(SBool):
    """
    .. admonition:: Truthy-Falsy Booleans

        A Boolean implementation whose distinct truthy and falsy
        values are distinct singleton subclasses, not just
        distinct singleton values.

        .. important::

            Do not subclass ``TF_Bool`` itself. Subclassing it is
            designed to fail at runtime.

        .. tip::

            Logically combine these using Python's bitwise operators.

        .. warning::

            Although these datastructures are completely compatible
            with Python shortcut evaluation, care needs to be taken
            when using them with the ``and``, ``or``, and ``not`` builtins.

            For example:

            - ``~ALWAYS is NEVER``
            - ``not ALWAYS is False``
            - ``(ALWAYS and False) is False``
            - ``(ALWAYS or False) is ALWAYS``

    """

    def __new__(cls, witness: object, flavor: Hashable = None) -> Self:
        """
        .. admonition:: __new__

            :param witness: Determines which subtype,
                            ``T_Bool`` or ``F_Bool``,
                            of ``TF_Bool`` to return.
            :param flavor: Ignored parameter, only two flavors,
                           one truthy and one falsy.
            :returns: The singleton truthy or singleton falsy instance.

        """
        if witness:
            return cast(Self, T_Bool())
        return cast(Self, F_Bool())

    def __init_subclass__(cls, **kwargs: object) -> None:
        """
        .. admonition:: __init_subclass__

            :raises TypeError: Fails at runtime if any attempt to
                    subclass is made.

        """
        super().__init_subclass__(**kwargs)
        if TF_Bool in cls.__bases__ and cls.__module__ != TF_Bool.__module__:
            msg = 'TF_Bool is sealed'
            raise TypeError(msg)

    def __invert__(self) -> TF_Bool:
        """
        .. admonition:: bitwise invert operator

            Inverts the value of an TF_Bool.

            :returns: The inverted value of the SBool.

        """
        if self:
            return F_Bool()
        return T_Bool()

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            A string to reproduce the TF_Bool.

            :returns: 'T_Bool()' if truthy, otherwise `F_Bool()`

        """
        if self:
            return 'T_Bool()'
        return 'F_Bool()'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            A string meaningful to an end user.

            :returns: 'ALWAYS' if truthy, otherwise 'NEVER'

        """
        if self:
            return 'ALWAYS'
        return 'NEVER'


@final
class T_Bool(TF_Bool):
    """
    .. admonition:: Truthy TF_Bool subclass

         Type of the truthy singleton ``TF_Bool`` instance.
         A distinct type from ``F_Bool``.

    """

    _lock: ClassVar[Lock] = Lock()

    def __new__(cls, witness: object = None, flavor: Hashable = None) -> Self:
        """
        .. admonition:: new

            :param witness: Ignored parameter, a T_Bool is always truthy.
            :param flavor: Ignored parameter, only one truthy "flavor"
            :returns: The truthy T_Bool singleton instance.

        """
        inst = cls.__dict__.get('_truthy')
        if inst is None:
            with T_Bool._lock:
                inst = cls.__dict__.get('_truthy')
                if inst is None:
                    inst = super(SBool, cls).__new__(cls, 1)
                    cls._truthy = inst
        return cast(Self, inst)

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if T_Bool in cls.__bases__ and cls.__module__ != T_Bool.__module__:
            msg = 'T_Bool is final'
            raise TypeError(msg)

    def __reduce__(self) -> tuple[type[T_Bool], tuple[()]]:
        """
        .. admonition:: reduce

            Tell ``pickle`` and ``copy`` how to reconstruct the
            ``T_Bool`` singleton: call ``T_Bool()`` rather than
            rebuilding the object directly.

            - reconstruction goes through ``__new__``, so the flavor
              cache is consulted
            - unpickling returns the existing singleton of that flavor,
              or creates and caches it in a fresh interpreter
            - ``copy`` and ``deepcopy`` use the same protocol, so they
              return the singleton unchanged

            :returns: The pair ``(TBool, ())``, which
                      ``pickle`` calls to rebuild the sentinel.

            .. important::

                Without this, ``pickle`` would construct a duplicate
                ``T_Bool`` outside the instance ``dict``, and ``is``
                comparisons against it would silently fail.

        """
        return (T_Bool, ())

    def __and__(self, other: int) -> int:
        """
        .. admonition:: bitwise and operator

            Overloading ``&`` to perform Boolean "and" if ``other``
            is another ``TF_Bool``.

            :param other: Any object derived from int.
            :returns: Boolean "and" if other is an SBool
                      otherwise returns bitwise "and".
            :rtype: First common ancestor of the types of self and other
                    if both of type SBool, otherwise int.

        """
        if isinstance(other, TF_Bool):
            return other
        return super().__and__(other)

    def __or__(self, other: int) -> int:
        """
        .. admonition:: bitwise or operator

            Overloading ``|`` to perform Boolean "or" if ``other``
            is another ``TF_Bool``.

            :param other: Any object derived from int.
            :returns: Boolean "or" if other is an SBool
                      otherwise returns bitwise "or".
            :rtype: First common ancestor of the types of self and other
                    if both of type SBool, otherwise int.

        """
        if isinstance(other, TF_Bool):
            return self
        return super().__or__(other)

    def __xor__(self, other: int) -> int:
        """
        .. admonition:: bitwise xor operator

            Overloading ``^`` to perform Boolean "xor" if ``other``
            is another ``TF_Bool``.

            :param other: Any object derived from int.
            :returns: Boolean "xor" if other is an SBool
                      otherwise returns bitwise "xor".
            :rtype: First common ancestor of the types of self and other
                    if both of type SBool, otherwise int.

        """
        if isinstance(other, TF_Bool):
            if other:
                return ~self
            return self
        return super().__xor__(other)


@final
class F_Bool(TF_Bool):
    """
    .. admonition:: Falsy TF_Bool subclass

         Type of the falsy singleton ``TF_Bool`` instance.
         A distinct type from ``T_Bool``.

    """

    _lock: ClassVar[Lock] = Lock()

    def __new__(cls, witness: object = None, flavor: Hashable = None) -> Self:
        """
        .. admonition:: new

            :param witness: Ignored parameter, an F_Bool is always falsy.
            :param flavor: Ignored parameter, only one falsy "flavor".
            :returns: The falsy F_Bool singleton instance.

        """
        inst = cls.__dict__.get('_falsy')
        if inst is None:
            with T_Bool._lock:
                inst = cls.__dict__.get('_falsy')
                if inst is None:
                    inst = super(SBool, cls).__new__(cls, 0)
                    cls._falsy = inst
        return cast(Self, inst)

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if F_Bool in cls.__bases__ and cls.__module__ != F_Bool.__module__:
            msg = 'F_Bool is final'
            raise TypeError(msg)

    def __reduce__(self) -> tuple[type[F_Bool], tuple[()]]:
        """
        .. admonition:: reduce

            Tell ``pickle`` and ``copy`` how to reconstruct the
            ``F_Bool`` singleton: call ``T_Bool()`` rather than
            rebuilding the object directly.

            - reconstruction goes through ``__new__``, so the flavor
              cache is consulted
            - unpickling returns the existing singleton of that flavor,
              or creates and caches it in a fresh interpreter
            - ``copy`` and ``deepcopy`` use the same protocol, so they
              return the singleton unchanged

            :returns: The pair ``(TBool, ())``, which
                      ``pickle`` calls to rebuild the sentinel.

            .. important::

                Without this, ``pickle`` would construct a duplicate
                ``T_Bool`` outside the instance ``dict``, and ``is``
                comparisons against it would silently fail.

        """
        return (F_Bool, ())

    def __and__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return self
        return super().__and__(other)

    def __or__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            return other
        return super().__or__(other)

    def __xor__(self, other: int) -> int:
        if issubclass(type(other), TF_Bool):
            if other:
                return other
            return self
        return super().__xor__(other)


ALWAYS: Final[TF_Bool] = T_Bool()
"""
.. admonition:: ALWAYS

    :var ALWAYS: The truthy singleton TF_Bool instance.

"""

NEVER: Final[TF_Bool] = F_Bool()
"""
.. admonition:: NEVER

    :var NEVER: The falsy singleton TF_Bool instance.

"""
