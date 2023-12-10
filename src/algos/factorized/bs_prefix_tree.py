from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from sortedcontainers import SortedDict

from monoid import MonoidElem
from universes import Universe


@dataclass
class PrefixTreeNode:
    string: MonoidElem
    value: Universe
    succ: SortedDict = field(default_factory=SortedDict)
    following: PrefixTreeNode | None = None

    def insert(self, string: MonoidElem, value: Universe):
        self.succ[string.last().letter()] = PrefixTreeNode(string, value)

    def find_node(self, string: MonoidElem) -> PrefixTreeNode | None:
        if len(string) == 0:
            return self

        next_node = self.succ.get(string.first().letter())
        if next_node is None:
            return None

        return next_node.find_node(string.suffix())

    def _calc_following(self):
        d = sorted(self.succ)
        for x, y in zip(d, d[1:]):
            self.succ[x].following = self.succ[y]

        for s in self.succ.values():
            assert type(s) == PrefixTreeNode
            s._calc_following()

    def first_succ(self):
        return self.succ[0]


class PrefixTree:
    root: PrefixTreeNode

    def __init__(self, bs: Iterable[tuple[MonoidElem, Universe]], id_val: Universe):
        self.root = PrefixTreeNode(MonoidElem.identity(), id_val)
        map(
            lambda x: self.insert(*x),
            sorted(
                list(bs),
                key=lambda x: x[0]
            )
        )
        self.root._calc_following()

    def find_node(self, string: MonoidElem):
        return self.root.find_node(string)

    def insert(self, string: MonoidElem, value: Universe):
        pref, suff = self.root.find_node(
            string.prefix()), self.root.find_node(string.suffix())
        if pref is None or suff is None:
            return
        pref.insert(string, value)

    def delete(self, string: MonoidElem):
        prefix = self.find_node(string)
        if prefix is None:
            return
        del prefix.succ[string.last().letter()]
