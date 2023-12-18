from __future__ import annotations
import itertools

from monoid import MonoidElem
from algos.factorized.bs_prefix_tree import PrefixTree, PrefixTreeNode
from universes import Transformation


def fill_tree(tree: PrefixTree, string: MonoidElem, sigma: list[int], l:int):
    tree.insert(string, Transformation([]))

    if l == 0:
        return
    
    for i in sigma:
        fill_tree(tree, string + MonoidElem.from_char(i), sigma, l-1)

sigma = [1,2,3,4]
tree = PrefixTree([], Transformation([]))
fill_tree(tree, MonoidElem.identity(), sigma, 5)
# print(tree)
w = MonoidElem([2,2])

print(f'w is {w}')
res = tree.search_superstrings(w)
print(f'res: {res}')


