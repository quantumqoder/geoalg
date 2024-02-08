from collections import UserDict
from math import ceil, comb, log2
from typing import Generator, Iterable, Iterator, List, Mapping, Optional, Sequence, Union

from base import Base, Bases
from blade import Blade
from type import CoeffType


class Multivector(UserDict):
    def __init__(self, *coeffs: Union[Mapping[int, Blade], CoeffType], dim: Optional[int] = None) -> None:
        UserDict.__init__(self)
        if isinstance((c0 := coeffs[0]), (dict, Mapping)):
            for key, val in c0.items():
                if not isinstance(key, int):
                    raise TypeError
                if key < 0:
                    raise ValueError
                if isinstance(val, Blade):
                    self[key] = val
                    continue
                if isinstance(val, (list, Sequence)):
                    

    
    def __init__(
        self,
        *coeffs: Union[
            Mapping[int, Union[Bases, Sequence[Union[int, float, Base]]]],
            CoeffType,
        ],
        dim: Optional[int] = None
    ) -> None:
        UserDict.__init__(self)
        if isinstance(coeffs[0], (dict, Mapping)):
            for key, val in coeffs[0].items():
                if not isinstance(key, int):
                    raise TypeError
                if key < 0:
                    raise ValueError
                if isinstance(val, Bases):
                    self[key] = val
                    continue
                if isinstance(val, Sequence):
                    for coeff in val:
                        if not isinstance(coeff, (int, float, Base)):
                            raise TypeError
                    self[key] = Bases(*val)
            return
        self.__coeffs: List[float] = []
        for coeff in coeffs:
            match coeff:
                case int() | float():
                    self.__coeffs.append(coeff)
                case list():
                    self.__coeffs.extend(coeff)
                case tuple() | set() | range() | Generator() | Iterator() | Iterable() | Sequence():
                    self.__coeffs.extend(list(coeff))
                case _:
                    raise TypeError
        self.__dim: int = ceil(log2(len(self.__coeffs)))
        if dim is not None and not isinstance(dim, int):
            raise TypeError
        if dim is not None and dim < 0:
            raise ValueError
        if dim is not None and dim < self.__dim:
            raise ValueError
        self.__coeffs += [0 for _ in range(2**dim - 2**self.__dim)]
        self.__dim = dim
        j: int = 0
        for i in range(self.__dim + 1):
            self[i] = Bases(*self.__coeffs[j: j + (C := comb(self.__dim, i))])
            j += C

    @property
    def dim(self) -> int:
        return self.__dim

    def __repr__(self) -> str:
        return super().__repr__()