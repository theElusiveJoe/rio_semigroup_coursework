from dataclasses import dataclass

from monoid import MonoidController, MonoidElem
from universes import Universe
from .easy_node import EasyNode


@dataclass
class SemigroupRepr:
    mc: MonoidController
    sigma: list[int]
    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]

    def get_rules(self):
        return {m: n.string for m, n in self.table.items() if n.value not in self.value_table}
