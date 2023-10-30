from __future__ import annotations
from typing import Iterable
from universes.abc_universe import Universe


class T(Universe):
    elems: tuple[int, ...]

    def __init__(self, elems: Iterable[int]) -> None:
        self.elems = tuple(elems)

    def __len__(self):
        return len(self.elems)

    def __repr__(self) -> str:
        return str(self.elems)
    
    def __mul__(self, other:T):
        new_elems = []
        for x in other.elems:
            new_elems.append(self.elems[x-1])

        return T(new_elems)
    
    def __eq__(self, other:T) -> bool:
        return self.elems == other.elems
    
    def __hash__(self) -> int:
        return hash(self.elems)
    
    @staticmethod
    def e():
        return T([1,2,3,4,5,6])