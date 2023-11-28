from __future__ import annotations
from dataclasses import dataclass, field

from universes import Universe
from monoid import MonoidElem


@dataclass
class Node:
    value: Universe
    first: MonoidElem   
    last: MonoidElem 
    prefix: MonoidElem     
    suffix: MonoidElem
    len: int
    next: MonoidElem
    pua: dict[int, MonoidElem] = field(default_factory=dict)
    pua_flag: dict[int, bool] = field(default_factory=dict)
    pau: dict[int, MonoidElem] = field(default_factory=dict)

    def retrieve_string(self) -> MonoidElem:
        if self.is_identity():
            return MonoidElem.identity()
        return self.first + self.suffix
    
    def is_identity(self):
        return self.first == MonoidElem([])
    
    def __repr__(self) -> str:
        return f'{self.retrieve_string()}[{self.value}]'