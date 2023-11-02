from __future__ import annotations
from typing import Iterable
from universes.abstract import Universe


class Transformation(Universe):
    elems: tuple[int, ...]

    def __init__(self, elems: Iterable[int]) -> None:
        self.elems = tuple(elems)

    def __len__(self):
        return len(self.elems)

    def __repr__(self) -> str:
        return str(self.elems)
    
    def __mul__(self, other:Transformation):
        new_elems = []
        for x in other.elems:
            new_elems.append(self.elems[x-1])

        return Transformation(new_elems)
    
    def __eq__(self, other:Transformation) -> bool:
        return self.elems == other.elems
    
    def __hash__(self) -> int:
        return hash(self.elems)
    
    def identity(self):
        return Transformation([i for i in range(1, len(self)+1)])