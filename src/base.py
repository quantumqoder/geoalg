from collections import UserList
from types import NotImplementedType
from typing import Self, Union


class Base:
    def __init__(self, __index: int) -> None:
        if not isinstance(__index, int):
            raise TypeError(f"{type(__index)} ({__index})")
        if __index < 0:
            raise ValueError(f"index should be non-negative")
        self.__index = __index

    def __repr__(self) -> str:
        return f"e{self.__index}"

    @property
    def index(self) -> int:
        return self.__index

    def __or__(self, __value: Self) -> Union[int, "Bases", NotImplementedType]:
        if not isinstance(__value, Base):
            return NotImplemented
        return self * __value if self.__index == __value.index else self ^ __value

    def __mul__(self, __other: Self) -> NotImplementedType:
        return NotImplementedType

    def __xor__(self, __other: Self) -> Union[Self, NotImplementedType]:
        if not isinstance(__other, Base):
            return NotImplemented
        return Bases(self, __other)


class Bases(UserList):
    def __init__(self, *bases: Union[int, float, Base]) -> None:
        UserList.__init__(self)
        for base in bases:
            if isinstance(base, int):
                self.append(Base(base))
                continue
            if isinstance(base, Base):
                self.append(base)
                continue
            raise TypeError(f"{type(base)} ({base})")

    def __repr__(self) -> str:
        return "".join(f"{base}" for base in self)

    def __or__(self, __value: Self) -> Union[Self, NotImplementedType]:
        if not isinstance(__value, Bases):
            return NotImplemented
        return Bases(*[b1 | b2 for b1 in self for b2 in self])
