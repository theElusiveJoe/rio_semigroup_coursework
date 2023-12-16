from dataclasses import dataclass
from sortedcontainers import SortedList

from monoid import MonoidController, MonoidElem
from universes import Universe

from .easy_node import EasyNode, MonoidElemKind
from .military_algo import MilitaryAlgo
from .semigroup_repr import SemigroupRepr
from .bs_prefix_tree import PrefixTree, PrefixTreeNode


@dataclass
class QueueElem:
    prefix: MonoidElem
    prefix_value: Universe
    bs_node: PrefixTreeNode
    kind: MonoidElemKind

    def __repr__(self) -> str:
        return f'{self.prefix}+{self.bs_node.string}'

    def to_string(self):
        return self.prefix + self.bs_node.string

    def get_value(self):
        return self.prefix_value * self.bs_node.value


class Queue:
    storage: list[QueueElem]

    def __init__(self):
        self.storage = list()

    def __repr__(self):
        return f'Q{str(self.storage)}'

    def __len__(self):
        return len(self.storage)

    def pop(self) -> QueueElem:
        return self.storage.pop(0)

    def add(self, e: QueueElem):
        self.storage.append(e)
