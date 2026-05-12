from .subtypable import SBool
from collections.abc import Hashable
from pythonic_fp.gadgets.sentinels.novalue import NoValue
from typing import Final

__all__ = ['TF_Bool', 'T_Bool', 'F_Bool', 'ALWAYS', 'NEVER']

class TF_Bool(SBool):
    def __new__(cls, witness: object, flavor: Hashable = ...) -> TF_Bool: ...

class T_Bool(TF_Bool):
    def __new__(cls, witness: object = ..., flavor: Hashable | NoValue = ...) -> T_Bool: ...

class F_Bool(TF_Bool):
    def __new__(cls, witness: object = ..., flavor: Hashable | NoValue = ...) -> F_Bool: ...

ALWAYS: Final[TF_Bool]
NEVER: Final[TF_Bool]
