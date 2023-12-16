from dataclasses import dataclass

from monoid import MonoidController, MonoidElem
from universes import Universe
from .easy_node import EasyNode


@dataclass
class SemigroupRepr:
    mc: MonoidController
    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]

    def get_rules(self):
        return {m: n.string for m, n in self.table.items() if n.value not in self.value_table}

    def draw_table(self):
        pairs = list(map(
            lambda x: (self.mc.to_string(x[0]), f'{self.mc.to_string(x[1].string)}'),
            self.table.items()
        ))

        print('Table:')
        for x,y in pairs:
            print(f'    {x} -> {y}')