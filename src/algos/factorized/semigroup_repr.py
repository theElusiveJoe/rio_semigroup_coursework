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

    def get_rules(self):
        return {m: n.string for m, n in self.table.items(
        ) if n.value not in self.value_table}

    def draw_table(self):
        print('Table:')
        for x, y in self.table.items():
            print(f'    {x} -> {y.string}')

    def get_srs(self):
        return {k: v.string for k, v in self.table.items()}

    def __eq__(self, o: SemigroupRepr):
        return self.get_srs() == o.get_srs()
