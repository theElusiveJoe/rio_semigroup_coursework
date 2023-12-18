from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum

from universes import Universe
from monoid import MonoidElem


class MonoidElemKind(IntEnum):
    A = 0
    B = 1

    def another(self):
        return MonoidElemKind((self + 1) % 2)


@dataclass
class EasyNode:
    value: Universe
    string: MonoidElem

    linked_strings: set[MonoidElem] = field(default_factory=set)
    heterogenic_linked_strings: set[MonoidElem] = field(default_factory=set)

    def __len__(self):
        return len(self.string)

    def __repr__(self) -> str:
        return f'{self.string}->{self.value}'

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, o: EasyNode) -> bool:
        return self.value == o.value and self.string == o.string

    def is_identity(self):
        return self.string.is_identity()
