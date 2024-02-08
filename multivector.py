import itertools
import math
from collections import UserDict
from types import GeneratorType
from typing import (Dict, Iterable, Iterator, List, Optional, Self, Set, Tuple,
                    Union)

from src.type import CoeffType


class Multivector(UserDict):
    def __init__(self, *coeffs: Union[Dict[int, List[float]], CoeffType], dim: Optional[int] = None) -> None:
        if isinstance(coeffs[0], dict):
            for key in coeffs[0]:
                if not isinstance(key, int):
                    raise TypeError(f"Key must be integer, {type(key)}")
                if key < 0:
                    raise ValueError(f"Key must be positive, {key}")
            UserDict.__init__(self, coeffs[0])
            self.__dim = len(self) - 1
        else:
            UserDict.__init__(self)
            self.__coeffs: List[float] = []
            for coeff in coeffs:
                match coeff:
                    case int() | float():
                        self.__coeffs.append(coeff)
                    case list():
                        self.__coeffs.extend(coeff)
                    case tuple() | set() | range() | GeneratorType() | Iterator() | Iterable():
                        self.__coeffs.extend(list(coeff))
                    case _:
                        raise TypeError(f"Unsupported type {type(coeff)} ({coeff})")
            self.__dim = math.ceil(math.log2(len(self.__coeffs)))
            self.__coeffs += [0 for _ in range(2**self.__dim - len(self.__coeffs))]
            if dim is not None:
                if not isinstance(dim, int):
                    raise TypeError(f"Dimension can't be non-integer, {type(dim)}")
                if dim < 0:
                    raise ValueError(f"Dimension can't be negative, {dim}")
                if dim < self.__dim:
                    raise ValueError(f"Dimension must be > {self.__dim}")
                self.__coeffs += [0 for _ in range(2**dim - 2**self.__dim)]
                self.__dim = dim
            j: int = 0
            for i in range(self.__dim + 1):
                self[i] = self.__coeffs[j : j + math.comb(self.__dim, i)]
                j += math.comb(self.__dim, i)

    @property
    def dim(self) -> int:
        return self.__dim

    def __str__(self) -> str:
        multi_vec: str = ""
        for grade, coeffs in self.items():
            for coeff, index in zip(coeffs, itertools.combinations(range(self.__dim), grade)):
                if coeff == 0:
                    continue
                if coeff < 0:
                    multi_vec = multi_vec[: -2] + "- "
                multi_vec += f"{abs(coeff)}^e{"".join(f"{ind}" for ind in index)} + "
        return multi_vec[: -3]

    def __repr__(self) -> str:
        return (
            f"{__class__.__name__}({self}, dim = {self.__dim})\n  "
            + "\n  ".join(f"{grade} -> {coeffs}" for grade, coeffs in self.items())
        )

    def __neg__(self) -> Self:
        return Multivector(-coeff for coeff in self.__coeffs)

    def __invert__(self) -> Self:
        blade_coeffs: List[float] = []
        op = 1
        for k, val in self.data.items():
            if k != 0 and k % 2 == 0:
                op *= -1
            for v in val:
                blade_coeffs.append(op * v)
        return Multivector(blade_coeffs)
        # return Multivector(self.__coeffs[::-1])
        # return Multivector(self.__coeffs[::2][::-1] + self.__coeffs[1::2])

    def __add__(self, __other: Self) -> Self:
        if not isinstance(__other, Multivector):
            return NotImplemented
        m1, m2 = (self, __other) if len(self) > len(__other) else (__other, self)
        return Multivector({grade: [v1 + v2 for v1, v2 in zip(m1.get(grade), m2.get(grade) + [0 for _ in range(len(m1.get(grade)) - len(m2.get(grade)))] if m2.get(grade) else [0 for _ in range(len(m1.get(grade)))])] for grade in m1})

    def __sub__(self, __other: Self) -> Self:
        return self + (-__other)
