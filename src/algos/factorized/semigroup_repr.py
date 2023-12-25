from __future__ import annotations
from dataclasses import dataclass
from pprint import pp

from monoid import MonoidController, MonoidElem
from universes import Universe
from .easy_node import EasyNode


@dataclass
class SemigroupRepr:
    mc: MonoidController
    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]
    sigma: set[int]

    def get_srs(self):
        return dict(
            (ls, node.string)
            for node in self.table.values()
            for ls in node.linked_strings
        )

    def __eq__(self, o: SemigroupRepr):
        return self.get_srs() == o.get_srs()
