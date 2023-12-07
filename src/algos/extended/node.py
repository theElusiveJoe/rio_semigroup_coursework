from __future__ import annotations
from dataclasses import dataclass, field
from universes.abstract import Universe
from monoid.element import MonoidElem


@dataclass
class ExtendedNode:
    value: Universe
    first: MonoidElem
    last: MonoidElem
    prefix: MonoidElem
    suffix: MonoidElem
    len: int
    next: MonoidElem
    pua: list[MonoidElem] = field(default_factory=list)
    pua_flag: list[bool] = field(default_factory=list)
    pau: list[MonoidElem] = field(default_factory=list)

    def retrieve_string(self) -> MonoidElem:
        if self.is_identity():
            return MonoidElem.identity()
        return self.first + self.suffix

    def is_identity(self):
        return self.first == MonoidElem([])
