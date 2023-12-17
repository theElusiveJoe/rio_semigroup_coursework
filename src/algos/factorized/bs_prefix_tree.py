from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from sortedcontainers import SortedDict

from monoid import MonoidElem
from universes import Universe
from utils.logger import log


@dataclass
class PrefixTreeNode:
    string: MonoidElem
    value: Universe
    succ: SortedDict = field(default_factory=SortedDict)
    following: PrefixTreeNode | None = None

    def get_graph(self, lvl):
        ss = []
        for next in self.succ.values():
            ss.append(f'{" "*2*lvl}{self.string} -> {next.string}')
            ss += next.get_graph(lvl+1)
        return ss

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

    def first_succ(self) -> PrefixTreeNode:
        return self.succ.values()[0]  # type: ignore


class PrefixTree:
    root: PrefixTreeNode

    def __init__(self, bs: list[tuple[MonoidElem, Universe]], id_val: Universe):
        self.root = PrefixTreeNode(MonoidElem.identity(), id_val)
        [self.insert(*x) for x in sorted(bs)]
        self.root._calc_following()

    def __repr__(self):
        return '\n'.join(self.root.get_graph(1))

    def find_node(self, string: MonoidElem):
        return self.root.find_node(string)

    def insert(self, string: MonoidElem, value: Universe):
        log(f'inserting {string}', lvl=2 )
        if string.is_identity():
            return
        pref, suff = self.root.find_node(
            string.prefix()), self.root.find_node(string.suffix())
        if pref is None or suff is None:
            return
        pref.insert(string, value)

    def delete(self, string: MonoidElem):
        prefix = self.find_node(string.prefix())
        if prefix is None:
            return
        del prefix.succ[string.last().letter()]
