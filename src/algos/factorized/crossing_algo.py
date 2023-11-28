from functools import cmp_to_key
from pprint import pp

from monoid import MonoidController, MonoidElem, RulesSystem
from universes import Universe
from .node import Node
from .military_algo import MilitaryAlgo


class CrossingAlgo:
    outer_mc: MonoidController

    sigma1: list[int]
    sigma2: list[int]

    table: dict[MonoidElem, Node] = dict()
    value_table: dict[Universe, Node] = dict()

    def __init__(self, a1: MilitaryAlgo, a2: MilitaryAlgo) -> None:
        self.outer_mc = a1.mc
        self.sigma1 = a1.sigma
        self.sigma2 = a2.sigma 
        self.merge_cayley_graphs(a1, a2)

    def run(self):
        pass

    def draw_table(self):
        print('Table:')
        for k, v in self.table.items():
            print(f'    {self.outer_mc.to_string(k)} -> ' +
                  f'{self.outer_mc.to_string(v.retrieve_string())}: {v.value}')
            
    def draw_value_table(self):
        print('Value Table:')
        for k, v in self.value_table.items():
            print(f'    {k} -> ' +
                  f'{self.outer_mc.to_string(v.retrieve_string())}: {v.value}')

    def merge_cayley_graphs(self, a1: MilitaryAlgo, a2: MilitaryAlgo):
        t1, vt1 = a1.table, a1.value_table
        t2, vt2 = a2.table, a2.value_table

        print(list(map(self.outer_mc.to_string, map(lambda x: x.retrieve_string(), vt1.values()))))
        print(list(map(self.outer_mc.to_string, map(lambda x: x.retrieve_string(), vt2.values()))))

        values1 = set(vt1.keys())
        values2 = set(vt2.keys())
        common_values = values1.intersection(values2)
        print(common_values)

        min_node = dict()
        # ищем узел с минимальным строковым значением
        # для всех пересекающихся значений в полугруппах
        for string, node in list(t1.items()) + list(t2.items()):
            if node.value in common_values:
                # выбираем ноду с минимальной строкой
                if min_node.get(node.value) is None:
                    min_node[node.value] = node
                else:
                    cur_string = min_node[node.value].retrieve_string()
                    prop_string = node.retrieve_string()
                    if self.outer_mc.compare(cur_string, prop_string) == 1:
                        min_node[node.value] = node
        pp(min_node)

        for string, node in list(t1.items()) + list(t2.items()):
            mn = node if node.value not in common_values else min_node[node.value]
            self.table[string] = mn
            self.value_table[node.value] = node

        self.draw_table()
        self.draw_value_table()
    
    def rearrange(self):
        all_basic_strings = list(map(lambda x: x.retrieve_string(), self.value_table.values()))
        all_basic_strings = sorted(
            all_basic_strings,
            key = cmp_to_key(self.outer_mc.compare)
        )
        print(list(map(self.outer_mc.to_string, all_basic_strings)))