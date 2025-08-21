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


"""Booleans which are either always "truthy" or always "falsy"."""

import threading
from collections.abc import Hashable
from typing import ClassVar, Final, final
from pythonic_fp.sentinels.novalue import NoValue
from ..subtypable import SBool

__all__ = [
    'TFSBool',
    'TSBool',
    'FSBool',
    'ALWAYS',
    'NEVER_EVER',
]


class TFSBool(SBool):
    """Rough idea"""

    def __new__(
        cls, witness: object, flavor: Hashable = NoValue()
    ) -> 'TFSBool':
        if witness:
            return TSBool()
        return FSBool()


@final
class TSBool(TFSBool):
    """The subtype of ``TFSBool`` which is always Truthy."""

    _truthy: 'ClassVar[TSBool | None]' = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(
        cls, witness: object = NoValue(), flavor: Hashable = NoValue()
    ) -> 'TSBool':
        """Get the ``TSBool`` always truthy singleton instance.

        :param witness: ignored parameter, always truthy"
        :param flavor: ignored parameter, only one truthy "flavor"
        :returns: the truthy ``TSBool`` singleton instance, an ``SBool`` subtype

        """
        if cls._truthy is None:
            with cls._lock:
                if cls._truthy is None:
                    cls._truthy = super(SBool, cls).__new__(cls, True)
        return cls._truthy

    def __repr__(self) -> str:
        return 'ALWAYS'

    def __invert__(self) -> SBool:
        return FSBool()


@final
class FSBool(TFSBool):
    """The subtype of ``SBool`` which is always Falsy."""

    _falsy: 'ClassVar[FSBool | None]' = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(
        cls, witness: object = NoValue(), flavor: Hashable = NoValue()
    ) -> 'FSBool':
        """Get the ``FSBool`` always falsy singleton instance.

        :param witness: parameter ignored, ``FSBool`` always falsy
        :param flavor: parameter ignored, only one falsy "flavor"
        :returns: the falsy ``FSBool`` singleton instance, an ``SBool`` subtype

        """
        if cls._falsy is None:
            with cls._lock:
                if cls._falsy is None:
                    cls._falsy = super(SBool, cls).__new__(cls, False)
        return cls._falsy

    def __repr__(self) -> str:
        return 'NEVER_EVER'

    def __invert__(self) -> SBool:
        return TSBool()


ALWAYS: Final[TSBool] = TSBool()  #: the truthy singleton of type ``TSBool``
NEVER_EVER: Final[FSBool] = FSBool()  #: the falsy singleton of type ``TSBool``
