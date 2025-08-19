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
    _truthy: ClassVar[TSBool | None]
    _lock: ClassVar[threading.Lock]

    def __new__(cls, ignored: bool = True) -> TSBool: ...
    def __repr__(self) -> str: ...
    def __invert__(self) -> SBool: ...

@final
class FSBool(SBool):
    _falsy: ClassVar[FSBool | None]
    _lock: ClassVar[threading.Lock]

    def __new__(cls, ignored: bool = False) -> FSBool: ...
    def __repr__(self) -> str: ...
    def __invert__(self) -> SBool: ...

ALWAYS: Final[TSBool]
NEVER_EVER: Final[FSBool]
