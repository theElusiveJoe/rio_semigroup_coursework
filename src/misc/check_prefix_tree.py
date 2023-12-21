from __future__ import annotations

import sys
sys.path.append(f'{sys.path[0]}/..')

from universes import Transformation
from algos.factorized.bs_prefix_tree import PrefixTree, PrefixTreeNode
from monoid import MonoidElem


def fill_tree(tree: PrefixTree, string: MonoidElem, sigma: list[int], l: int):
    tree.insert(string, Transformation([]))
    assert tree.find_node(string) is not None, print(f'insert failed {string}')

    if l == 0:
        return

    for i in sigma:
        fill_tree(tree, string + MonoidElem.from_char(i), sigma, l - 1)


sigma = [1, 2, 3]
tree = PrefixTree([], Transformation([]))
fill_tree(tree, MonoidElem.identity(), sigma, 5)
print(tree)
w = MonoidElem([1])

print(f'w is {w}')
res = tree.delete_all_superstrings_from_table_and_tree(w, {})
print(tree)
