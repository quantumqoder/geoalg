import itertools
from collections import UserList
from types import GeneratorType
from typing import Iterable, Iterator, Optional, Union

from base import Bases
from type import CoeffType


class Blade(UserList):
    def __init__(self, grade: int, *coeffs: CoeffType, dim: Optional[int] = None) -> None:
        UserList.__init__(self)
        if not isinstance(grade, int):
            raise TypeError("grade must be an integer")
        if grade < 0:
            raise ValueError("grade must be non-negative")
        self.__grade = grade
        for coeff in coeffs:
            match coeff:
                case int() | float():
                    self.append((coeff, None))
                case list() | tuple () | set() | GeneratorType() | Iterable() | Iterator():
                    self.extend([(cff, None) for cff in coeff])
                case _:
                    raise TypeError(f"{type(coeff)} ({coeff})")
        if dim is not None and not isinstance(dim, int):
            raise TypeError("dim must be an integer")
        if dim is not None and dim < 0:
            raise ValueError("dim must be positive")
        if dim is not None and dim < len(self):
            raise ValueError(f"dim must be >= {len(self)}")
        self.extend([(0, None) for _ in range((dim or 0) - len(self))])
        if (self.__grade == 0 or self.__grade == len(self)) and len(self) > 0:
            raise ValueError(f"Blade-{self.__grade} can't have multiple components")
        if self.__grade > len(self):
            raise ValueError(
                f"Insufficient values provided. Max {self.__grade + 1} required"
            )
        UserList.__init__(self, [(coeff, Bases(*index)) for (coeff, _), index in zip(self, itertools.combinations(range(len(self)), self.__grade))])

    @property
    def grade(self) -> int:
        return self.__grade

    @property
    def dim(self) -> int:
        return len(self) if self.__grade > 0 else 0

    @dim.setter
    def dim(self, __dim: int) -> None:
        if __dim < self.dim:
            raise ValueError(f"dim must be >= {self.dim}")
        self.__init__(self.__grade, *[coeff for (coeff, _) in self], dim=__dim)

    def __str__(self) -> str:
        blade: str = ""
        for (coeff, base) in self:
            if coeff == 0:
                continue
            if coeff < 0:
                blade = blade[:-2] + "- "
            blade += f"{abs(coeff)}^{base} + "
        return blade[:-3]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({", ".join(f"{coeff}" for (coeff, _) in self)}), grade = {self.__grade}, dim = {self.dim}"

class Scalar(Blade):
    def __init__(self, coeffs: Union[int, float]) -> None:
        Blade.__init__(self, 0, coeffs)

class Vector(Blade):
    def __init__(self, *coeffs: CoeffType, dim: Optional[int] = None) -> None:
        Blade.__init__(self, 1, *coeffs, dim=dim)

class Bivector(Blade):
    def __init__(self, *coeffs: CoeffType, dim: Optional[int] = None) -> None:
        Blade.__init__(self, 2, *coeffs, dim=dim)

class Trivector(Blade):
    def __init__(self, *coeffs: CoeffType, dim: Optional[int] = None) -> None:
        Blade.__init__(self, 3, *coeffs, dim=dim)


if __name__ == "__main__":
    # print(Blade(5, 1, 2, 3, 4, 5, 6, dim=7))
    # print(repr(Blade(5, 1, 2, 3, 4, 5, 6, dim=7)))
    b = Blade(5, 1, 2, 3, 4, 5, 6)
    print(b)
    print(repr(b))
    b.dim = 9
    print(b)
    print(repr(b))
