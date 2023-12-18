from __future__ import annotations
import itertools

from monoid import MonoidElem
from universes import Universe
from utils.logger import log
from .bs_prefix_tree_node import PrefixTreeNode


class PrefixTree:
    root: PrefixTreeNode

    def __init__(
            self, bs: list[tuple[MonoidElem, Universe]], id_val: Universe, sort_bs=False):
        self.root = PrefixTreeNode(MonoidElem.identity(), id_val)
        if sort_bs:
            bs.sort()
        [self.insert(*x) for x in bs]
        self.root._calc_following()

    def __repr__(self):
        return '\n'.join(self.root.get_graph(1))

    def find_node(self, string: MonoidElem):
        return self.root.find_node(string)

    def insert(self, string: MonoidElem, value: Universe):
        log(f'inserting {string}', lvl=2)
        if string.is_identity():
            return
        pref = self.root.find_node(string.prefix())
        assert pref is not None
        pref.attach(string, value)

    def delete(self, string: MonoidElem):
        prefix = self.find_node(string.prefix())
        if prefix is None:
            return
        del prefix.succ[string.last().letter()]

    def search_superstrings(self, w: MonoidElem, ret_w=False):
        def rec_foo(w_node: PrefixTreeNode, ret_w=False):
            # {wx | x in SIGMA*}
            wx_strings = w_node.get_all_existing_postfix_superstrings(
                ret_self=ret_w)
            # {yw | y in SIGMA}
            yw_nodes = list(filter(None, [node.find_node(w_node.string)
                                          for node in self.root.get_succ_nodes()]))

            return wx_strings | set(itertools.chain(
                *[rec_foo(node, ret_w=True) for node in yw_nodes if node is not None]))

        w_node = self.find_node(w)
        if w_node is None:
            return set()

        return rec_foo(w_node, ret_w=False)
