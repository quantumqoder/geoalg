from types import GeneratorType
from typing import Iterable, Iterator, List, Set, Tuple, Union


type CoeffType = Union[
    float,
    List[float],
    Tuple[float],
    Set[float],
    GeneratorType[float],
    Iterable[float],
    Iterator[float],
    range,
]