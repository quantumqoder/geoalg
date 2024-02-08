from typing import Dict, List

from base import Base, generate_bases


def generate_algebra(p: int = 0, n: int = 0, z: int = 0) -> Dict[int, List[Base]]:
    return generate_bases(p + n + z)
