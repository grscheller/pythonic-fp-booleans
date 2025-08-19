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


"""Booleans which are either always true or always false."""

import threading
from typing import ClassVar, Final, final
from ..subtypable_boolean import SBool 

__all__ = [
    'TSBool',
    'FSBool',
    'ALWAYS',
    'NEVER_EVER',
]


@final
class TSBool(SBool):
    """**SBool truthy subtype**

    Can fully interact with ``FSBool`` and ``SBool`` types.
    """

    _truthy: 'ClassVar[TSBool | None]' = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, ignored: bool = True) -> 'TSBool':
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
class FSBool(SBool):
    """Falsy SBool subtype."""

    _falsy: 'ClassVar[FSBool | None]' = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, ignored: bool = False) -> 'FSBool':
        if cls._falsy is None:
            with cls._lock:
                if cls._falsy is None:
                    cls._falsy = super(SBool, cls).__new__(cls, False)
        return cls._falsy

    def __repr__(self) -> str:
        return 'NEVER_EVER'

    def __invert__(self) -> SBool:
        return TSBool()


ALWAYS: Final[TSBool] = TSBool()
NEVER_EVER: Final[FSBool] = FSBool()
