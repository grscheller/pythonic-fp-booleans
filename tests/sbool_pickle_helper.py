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

"""Pickle tests for subtypable booleans."""

from collections.abc import Hashable
from threading import Lock
from typing import ClassVar, Final, Self

from pythonic_fp.booleans.subtypable import SBool

__all__ = ['DBool', 'YES', 'NO']


class DBool(SBool):
    _truthy_lock: ClassVar[Lock] = Lock()
    _falsy_lock: ClassVar[Lock] = Lock()

    def __new__(cls, witness: object, flavor: Hashable = None) -> Self:
        """
        .. admonition:: new

            :param witness: Determines truthiness of the ``DBool``.
            :param flavor: Ignored, here for Liskov  substitution principle
            :returns: The truthy or falsy ``SBool`` class instance.

        """
        if witness:
            inst = cls.__dict__.get('_truthy')
            if inst is None:
                with DBool._truthy_lock:
                    inst = cls.__dict__.get('_truthy')
                    if inst is None:
                        inst = super(SBool, cls).__new__(cls, 1)
                        cls._truthy = inst
            return inst
        else:
            inst = cls.__dict__.get('_falsy')
            if inst is None:
                with DBool._falsy_lock:
                    inst = cls.__dict__.get('_falsy')
                    if inst is None:
                        inst = super(SBool, cls).__new__(cls, 0)
                        cls._falsy = inst
            return inst


YES: Final[DBool] = DBool(1)

NO: Final[DBool] = DBool(0)
