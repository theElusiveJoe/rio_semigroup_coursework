from __future__ import annotations

from functools import cmp_to_key
from pprint import pp
from copy import copy
from enum import IntEnum
from dataclasses import dataclass
from typing import NamedTuple

from sortedcontainers import SortedList

from monoid import MonoidController, MonoidElem
from universes import Universe

from .easy_node import EasyNode, MonoidElemKind
from .military_algo import MilitaryAlgo
from .semigroup_repr import SemigroupRepr
from .crossing_queue import QueueElem, Queue
from .bs_prefix_tree import PrefixTree, PrefixTreeNode


class CrossingAlgo:
    mc: MonoidController

    sr1: SemigroupRepr
    sr2: SemigroupRepr

    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]

    # bs_x: list[MonoidElem]
    # bs_y: list[MonoidElem]
    # bs_x_set: set[MonoidElem]
    # bs_y_set: set[MonoidElem]
    bs: PrefixTree
    ps_y: PrefixTree

    queue: Queue

    def __init__(self, sr1: SemigroupRepr, sr2: SemigroupRepr) -> None:
        self.mc = sr1.mc

        self.sr1, self.sr2 = sr1, sr2

        self.table = dict()
        self.value_table = dict()
        self.queue = Queue()

        bs_A: PrefixTree
        bs_B: PrefixTree

    def another_bs_kind(self, kind: MonoidElemKind):
        return {
            MonoidElemKind.A: self.bs_A,
            MonoidElemKind.B: self.bs_B,
        }[kind]

    def run(self):
        pass

    def merge_cayley_graphs(self):
        values1, values2 = set(self.sr1.value_table.keys()), set(
            self.sr2.value_table.keys())
        common_values = values1.intersection(values2)

        for cv in common_values:
            n1, n2 = self.sr1.value_table[cv], self.sr2.value_table[cv]
            table, value_table, node, short_node = (
                (self.sr2.table, self.sr2.value_table, n2, n1)
                if n1.string < n2.string
                else (self.sr1.table, self.sr1.value_table, n1, n2)
            )

            # убираем ноду из  таблицы значений
            del value_table[cv]
            table[node.string] = short_node

            # заменяем правила редукции
            for ls in node.linked_strings:
                table[ls] = short_node
                short_node.linked_strings.add(ls)

        # соберем вместе две таблицы
        self.table = {**self.sr1.table, **self.sr2.table}
        self.value_table = {**self.sr1.value_table, **self.sr2.value_table}

        # строим дерево базовых строк
        self.bs_A = PrefixTree(
            bs=map(lambda val, node: (val, node.string),  # type: ignore
                   self.sr1.value_table.items()),
            id_val=self.mc.identity(),
        )
        self.bs_B = PrefixTree(
            bs=map(lambda val, node: (val, node.string),  # type: ignore
                   self.sr2.value_table.items()),
            id_val=self.mc.identity(),
        )

        # self.draw_table()
        # self.draw_value_table()

    def setup_queue(self):
        self.queue.add(
            QueueElem(
                prefix=MonoidElem.identity(),
                prefix_value=self.mc.identity(),
                bs_node=self.bs_A.root.first_succ(),
                kind=MonoidElemKind.A,
            )
        )
        self.queue.add(
            QueueElem(
                prefix=MonoidElem.identity(),
                prefix_value=self.mc.identity(),
                bs_node=self.bs_B.root.first_succ(),
                kind=MonoidElemKind.B,
            )
        )

    def calc_crossing(self):

        while len(self.queue) > 0:
            # выдергиваем следующий из очереди
            qelem = self.queue.pop()

            # добавляем following
            if qelem.bs_node.following is not None:
                self.queue.add(
                    QueueElem(
                        prefix=qelem.prefix,
                        prefix_value=qelem.prefix_value,
                        bs_node=qelem.bs_node.following,
                        kind=qelem.kind,
                    )
                )

            switch_kind_nodes = self.another_bs_kind(qelem.kind).root.succ
            succ_nodes = qelem.bs_node.succ

            sk_index, sn_index = 0, 0

            def next_switch_kind():
                return QueueElem(
                    qelem.to_string() + qelem.bs_node.string,
                    qelem.prefix_value * qelem.bs_node.value,
                    switch_kind_nodes[sk_index],
                    qelem.kind.another(),
                )

            def next_succ():
                return QueueElem(
                    qelem.to_string(),
                    qelem.prefix_value,
                    succ_nodes[sn_index],
                    qelem.kind,
                )

            # перебераем все валидные строки
            while True:
                match sk_index < len(switch_kind_nodes), sn_index < len(succ_nodes):
                    case False, False:
                        break
                    case True, False:
                        # switch kind
                        new_qelem = next_switch_kind()
                        sk_index += 1
                    case False, True:
                        # succ
                        new_qelem = next_succ()
                        sn_index += 1
                    case _, _:
                        # сравниваем два варианта по последней букве
                        if switch_kind_nodes.keys.get(sk_index) < succ_nodes.get(sn_index):
                            # switch kind вариант предпочтительнее
                            new_qelem = next_switch_kind()
                            sk_index += 1
                        else:
                            # succ вариант предпочтительнее
                            new_qelem = next_succ()
                            sn_index += 1

                # ua - это базовая строка - т.е. prefix = eps
                # то не надо ничего проверять - ua и так минимальная c таким значением из рассмотренных ранее
                # просто добавим ее в очередь
                if new_qelem.prefix.is_identity():
                    self.queue.add(new_qelem)

                ua = new_qelem.to_string()
                sa = ua.suffix()
                sa_node = self.table.get(sa)

                # sa сократима, если ее нет в таблице, или она редуцируется
                if sa_node is None or sa_node.string != sa:
                    continue

                # найдем значение ua
                ua_val = new_qelem.get_value()
                # и поищем ноду с таким значением
                ua_min_node = self.value_table.get(ua_val)

                # мы нашли новое значение
                if ua_min_node is None:
                    new_node = EasyNode(
                        value=ua_val,
                        string=ua,
                    )
                    self.table[ua] = new_node
                    self.value_table[ua_val] = new_node
                    # добавляем новую строку в очередь
                    self.queue.add(new_qelem)
                    continue

                # такое значение есть, и эта строка не превосходит уже найденную
                if ua_min_node.string < ua:
                    self.table[ua] = ua_min_node
                    ua_min_node.linked_strings.add(ua)

                # такое значение есть, но оно меньше уже найденного
                old_node = ua_min_node
                # создаем новый узел
                new_node = EasyNode(
                    value=ua_val,
                    string=ua,
                )
                # записываем новый узел в таблицы
                self.table[ua] = new_node
                self.value_table[ua_val] = new_node
                # старая строка редуцируется к новой
                self.table[old_node.string] = new_node
                # и все строки, которые к ней редуцировались - тоже
                for ls in old_node.linked_strings:
                    self.table[ls] = new_node
                # если старый узел содержал базовую строку,
                # то эту базовую строку надо удалить из bs_tree,
                # чтобы больше не использовать ни эту строку, ни ее потомков
                self.bs_A.delete(old_node.string)
                self.bs_B.delete(old_node.string)

                # ну и добавляем в очередь
                self.queue.add(new_qelem)
