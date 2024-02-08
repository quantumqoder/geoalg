import itertools
import math
from collections import UserList
from types import GeneratorType
from typing import Dict, Iterable, Iterator, Optional, Self, Union
from src.multivector import Multivector

from src.type import CoeffType


class Blade(UserList):
    def __init__(self, grade: int, *coeffs: CoeffType, dim: Optional[int] = None) -> None:
        UserList.__init__(self)
        if not isinstance(grade, int):
            raise TypeError("grade must be an integer")
        if grade < 0:
            raise ValueError("grade must be positive")
        self.__grade = grade
        if self.__grade == 0 and len(coeffs) > 1:
            raise ValueError(f"Blade-{self.__grade} can't have multiple components")
        for coeff in coeffs:
            match coeff:
                case int() | float():
                    self.append(coeff)
                case list():
                    self.extend(coeff)
                case tuple() | set() | range() | GeneratorType() | Iterator() | Iterable():
                    self.extend(list(coeff))
                case _:
                    raise TypeError(f"Invalid type {type(coeff)} ({coeff})")
        if dim is not None and not isinstance(dim, int):
            raise TypeError("dim must be an integer")
        if dim is not None and dim < 0:
            raise ValueError("dim must be positive")
        if dim is not None and dim < len(coeffs):
            raise ValueError(f"dim must be >= {len(coeffs)}")
        self.extend([0 for _ in range(dim or 0 - len(coeffs))])

    @property
    def grade(self) -> int:
        return self.__grade

    @property
    def dim(self) -> int:
        return len(self) if self.__grade > 0 else 0
    
    @dim.setter
    def dim(self, __dim: int) -> None:
        if self.dim > __dim:
            raise Exception(f"Can't truncate {self.__class__.__name__.lower()}")
        self.extend([0 for _ in range(__dim - self.dim)])

    def __str__(self) -> str:
        blade: str = ""
        for coeff, index in zip(self, itertools.combinations(range(self.dim), self.__grade)):
            if coeff == 0:
                continue
            if coeff < 0:
                blade = blade[: -2] +  "- "
            blade += f"{abs(coeff)}^e{"".join(f"{b}" for b in index)} + "
        return blade[: -3]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({", ".join(f"{coeff}" for coeff in self)}), grade = {self.grade}, dim = {self.dim}"

    def __delitem__(self, __key: int) -> None:
        if not isinstance(__key, int):
            raise TypeError("index must be an integer")
        self.data[__key] = 0

    def __add__(self, __other: Self) -> Union[Self, Multivector]:
        if self.__grade == __other.grade:
            b1, b2 = (self, __other) if len(self) >= len(__other) else (__other, self)
            b2.dim = b1.dim
            return Blade(self.__grade, *[a + b for a, b in zip(b1, b2)]) if self.__class__ == Blade else self.__class__(*[a + b for a, b in zip(b1, b2)])
        b1, b2 = (self, __other) if self.__grade > __other.grade else (__other, self)
        return Multivector()

    def __mul__(self, other):
        return Blade(self.data * other)

    def __truediv__(self, other):
        return Blade(self.data / other)

    def __floordiv__(self, other):
        return Blade(self.data // other)

    def __mod__(self, other):
        return Blade(self.data % other)

class Vector(Blade):
    def __init__(
        self, *coeffs: CoeffType, dim: Optional[int] = None
    ) -> None:
        Blade.__init__(self, 1, *coeffs, dim = dim)

class Bivector(Blade):
    def __init__(
        self, *coeffs: CoeffType, dim: Optional[int] = None
    ) -> None:
        Blade.__init__(self, 2, *coeffs, dim = dim)

class Trivector(Blade):
    def __init__(
        self, *coeffs: CoeffType, dim: Optional[int] = None
    ) -> None:
        Blade.__init__(self, 3, *coeffs, dim = dim)

def gen_num_base_blades(dim: int) -> Dict[int, int]:
    return {k: math.comb(dim, k)  for k in range(dim + 1)}
