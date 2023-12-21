from __future__ import annotations
from dataclasses import dataclass, field
from sortedcontainers import SortedDict
from typing import Any

from monoid import MonoidElem
from universes import Universe
from utils.logger import log


@dataclass
class PrefixTreeNode:
    string: MonoidElem
    value: Universe
    succ: SortedDict = field(default_factory=SortedDict)
    following: PrefixTreeNode | None = None
    preceding: PrefixTreeNode | None = None

    def __repr__(self):
        return f'Node({self.string})'

    def get_graph(self, lvl):
        '''
        возвращает список строк, описывающих данное поддерево
        '''
        ss = []
        for next in self.succ.values():
            ss.append(
                f'{" "*2*lvl}{self.string} -> {next.string}( {next.preceding}, {next.following} )')
            ss += next.get_graph(lvl + 1)
        return ss

    def get_succ(self, i: int) -> PrefixTreeNode | None:
        '''
        обертка для метода get словаря succ
        '''
        return self.succ.get(i)

    def get_first_succ(self) -> PrefixTreeNode | None:
        '''
        возвращшает потомка с минимальной подстрокой.
        если потомков нет, то None
        '''
        if len(self.succ) == 0:
            return None
        return self.succ.values()[0]  # type: ignore

    def get_succ_keys(self) -> list[int]:
        '''
        возвращает сортированный список ключей словаря succ
        '''
        return list(self.succ.keys())

    def get_succ_nodes(self) -> list[PrefixTreeNode]:
        '''
        возвращает сортированный список значений словаря succ
        '''
        return list(self.succ.values())

    def attach(self, string: MonoidElem, value: Universe):
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
            self.succ[y].preceding = self.succ[x]

        for s in self.succ.values():
            assert isinstance(s, PrefixTreeNode)
            s._calc_following()

    def get_all_existing_postfix_superstrings(
            self, ret_self=False) -> set[MonoidElem]:
        res = set([self.string]) if ret_self else set()

        for next in self.succ.values():
            res |= next.get_all_existing_postfix_superstrings(ret_self=True)

        return res

    def rm_all_super_prefixes_from_table_and_tree(
            self, table: dict[MonoidElem, Any], rm_self=False):
        if self.string not in table:
            return
        if rm_self:
            table[self.string].linked_strings.discard(self.string)
            del table[self.string]

        for next in self.succ.values():
            next.rm_all_super_prefixes_from_table_and_tree(table, rm_self=True)
