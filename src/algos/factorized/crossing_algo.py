from __future__ import annotations

from operator import attrgetter
from pprint import pp

from universes import Universe
from monoid import MonoidController, MonoidElem
from utils.logger import log

from .bs_prefix_tree import PrefixTree
from .crossing_queue import QueueElem, Queue
from .semigroup_repr import SemigroupRepr
from .military_algo import MilitaryAlgo
from .easy_node import EasyNode, MonoidElemKind


class CrossingAlgo:
    mc: MonoidController
    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]

    sr1: SemigroupRepr
    sr2: SemigroupRepr

    bs_A: PrefixTree
    bs_B: PrefixTree

    queue: Queue

    def __init__(self, sr1: SemigroupRepr, sr2: SemigroupRepr) -> None:
        self.mc = sr1.mc
        self.sr1, self.sr2 = sr1, sr2

    def another_bs_kind(self, kind: MonoidElemKind):
        return {
            MonoidElemKind.A: self.bs_B,
            MonoidElemKind.B: self.bs_A,
        }[kind]
    
    def is_homogenious(self, string: MonoidElem):
        return all(map(lambda x: x in self.sr1.sigma, string.symbols)) or all(map(lambda x: x in self.sr2.sigma, string.symbols))

    def string_in_one_of_trees(self, string: MonoidElem):
        return bool(self.bs_A.find_node(string) or self.bs_B.find_node(string))

    def run(self):
        log('CROSSING ALGO')

        self.grow_bs_prefix_tree()
        self.merge_cayley_graphs()
        self.setup_queue()
        self.calc_crossing()
        self.normalize_linked_strings()

        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.table,
            self.value_table,
            self.sr1.sigma | self.sr2.sigma  
        )

    def grow_bs_prefix_tree(self):
        # строим дерево базовых строк
        log('TREE GROWING STARTED')

        self.bs_A = PrefixTree(
            bs=[(node.string, val)
                for val, node in self.sr1.value_table.items() if val != self.mc.identity()],
            id_val=self.mc.identity(),
        )
        self.bs_B = PrefixTree(
            bs=[(node.string, val)
                for val, node in self.sr2.value_table.items() if val != self.mc.identity()],
            id_val=self.mc.identity(),
        )

    def rm_bs_from_table_and_trees(self, string: MonoidElem, table: dict | None):
        if table is None:
            table = self.table
        self.bs_A.delete_all_superstrings_from_table_and_tree(string, table)
        self.bs_A.delete_all_superstrings_from_table_and_tree(string, table)

    def merge_cayley_graphs(self):
        values1, values2 = set(self.sr1.value_table.keys()), set(
            self.sr2.value_table.keys())
        values1.discard(self.mc.identity())
        values2.discard(self.mc.identity())
        common_values = values1.intersection(values2)

        log(f'values A: {values1}', lvl=2)
        log(f'values B: {values2}', lvl=2)
        log(f'values COMMON: {common_values}', lvl=2)

        log('MERGE STARTED')
        for cv in common_values:
            log(f'cv: {cv}', lvl=2)
            n1, n2 = self.sr1.value_table[cv], self.sr2.value_table[cv]
            log(f'node1: {n1}', lvl=3)
            log(f'node2: {n2}', lvl=3)
            log(f'node1 {"<" if n1.string < n2.string else ">"} node2', lvl=3)

            if n1.string < n2.string:
                table, value_table = self.sr2.table, self.sr2.value_table
                node, short_node = n2, n1
                tree_with_big_string = self.bs_B
            else:
                table, value_table = self.sr1.table, self.sr1.value_table
                node, short_node = n1, n2
                tree_with_big_string = self.bs_A

            # убираем ноду из таблицы значений
            del value_table[cv]

            # node.string -> short_node.string
            log(f'link {node.string} to {short_node.string}', lvl=3)
            # IGNORE LINKED STRINGS
            # table[node.string] = short_node
            short_node.linked_strings.add(node.string)
            log(f'link {node.linked_strings} to {short_node.string}', lvl=3)
            short_node.linked_strings |= node.linked_strings

            # удаляем node.string из prefix_tree
            log(f'rm {node.string} and all its superstrings from prefix trees and table', lvl=3)
            tree_with_big_string.delete_all_superstrings_from_table_and_tree(
                node.string, table)

            # IGNORE LINKED STRINGS
            # for ls in node.linked_strings:
                # table[ls] = short_node

        # соберем вместе две таблицы
        self.table = {**self.sr1.table, **self.sr2.table}
        self.value_table = {**self.sr1.value_table, **self.sr2.value_table}

    def setup_queue(self):
        log('SETTING UP QUEUE')
        self.queue = Queue()

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
        log(f'now queue is {self.queue}', lvl=2)

    def calc_crossing(self):
        log('CROSSING STARTED')
        while len(self.queue) > 0:
            # выдергиваем следующий из очереди
            log(f'now queue is {self.queue}', lvl=2)

            qelem = self.queue.pop()
            log(f'u = {qelem}', lvl=2)

            # добавляем following
            if qelem.bs_node.following is not None:
                next_qelem = QueueElem(
                    prefix=qelem.prefix,
                    prefix_value=qelem.prefix_value,
                    bs_node=qelem.bs_node.following,
                    kind=qelem.kind,
                )
                self.queue.add(next_qelem)
                log(f'add {next_qelem} to queue', lvl=3)

            # конструируем множества следующих строк
            # нужно только для лога 
            switch_kind_nodes = self.another_bs_kind(
                qelem.kind).root.get_succ_nodes()
            succ_nodes = qelem.bs_node.get_succ_nodes()
            log(
                f'switch kind variants: {list(map(attrgetter("string"), switch_kind_nodes))}',
                lvl=3)
            log(
                f'succ nodes variants: {list(map(attrgetter("string"), succ_nodes))}',
                lvl=3)
            
            sk_node = self.another_bs_kind(qelem.kind).root.get_smallest_succ()
            succ_node = qelem.bs_node.get_smallest_succ()

            def next_switch_kind():
                log('this is switch kind', lvl=4)
                return QueueElem(
                    qelem.to_string(),
                    qelem.prefix_value * qelem.bs_node.value,
                    sk_node,  # type: ignore
                    qelem.kind.another(),
                )

            def next_succ():
                log('this is next succ', lvl=4)
                return QueueElem(
                    qelem.prefix,
                    qelem.prefix_value,
                    succ_node,  # type: ignore
                    qelem.kind,
                )

            log('iterate succ and switch_kind', lvl=3)
            # перебераем все следующие строки
            while True:
                match sk_node, succ_node:
                    case None, None:
                        break
                    case _, None:
                        # switch kind
                        new_qelem = next_switch_kind()
                        sk_node = sk_node.following # type: ignore
                    case None, _:
                        # succ
                        new_qelem = next_succ()
                        succ_node = succ_node.following # type: ignore
                    case _, _:
                        # сравниваем два варианта по последней букве
                        if sk_node.string.last() < succ_node.string.last(): # type: ignore
                            # switch kind вариант предпочтительнее
                            new_qelem = next_switch_kind()
                            sk_node = sk_node.following # type: ignore
                        else:
                            # succ вариант предпочтительнее
                            new_qelem = next_succ()
                            succ_node = succ_node.following # type: ignore  

                log(f'ua = {new_qelem}', lvl=5)

                # ua - это базовая строка - т.е. prefix = eps
                # ua только что вышел из prefix tree, 
                # значит он точно никуда не редуцируется
                # и есть в таблицах
                # просто добавим ее в очередь
                if new_qelem.prefix.is_identity():
                    self.queue.add(new_qelem)
                    log('new_qelem in basic strings: just add it to queue', lvl=5)
                    continue

                ua = new_qelem.to_string()
                sa = ua.suffix()
                sa_node = self.table.get(sa)

                # sa редуцируема, если ее нет в таблице
                if sa_node is None:
                    log('new_qelem in is reducable: skip', lvl=5)
                    continue
                
                log(f'sa is {sa} and it is not reducable! {self.table.get(sa)}!=None', lvl=5)

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
                    log('new_qelem_val is new: add to queue', lvl=5)
                    continue

                # такое значение есть, и эта строка не превосходит уже
                # найденную
                if ua_min_node.string < ua:
                    log(f'{ua_min_node.string}, {ua} {"<" if ua_min_node.string < ua else ">"}', lvl=5)
                    log(f'{ua_min_node.string}, {ua} {"<" if ua_min_node.string < ua else ">"}', lvl=5)
                    ua_min_node.heterogenic_linked_strings.add(ua)
                    log(
                        f'string with such value exists {ua_min_node.string} and less than ua: just link ua to it', lvl=5)
                    continue

                # такое значение есть,
                # ua < ua_min_string
                # значит, ua_min_string - гомогенная
                old_node = ua_min_node
                log(
                    f'string with such value exists {old_node.string}, but ua is less', lvl=5)
                # создаем новый узел
                new_node = EasyNode(
                    value=ua_val,
                    string=ua,
                )
                
                # записываем новый узел в таблицы
                self.table[ua] = new_node
                self.value_table[ua_val] = new_node

                log(f'link {old_node.linked_strings} and {old_node.heterogenic_linked_strings} to {ua}', lvl=5)
                new_node.linked_strings |= old_node.linked_strings
                new_node.heterogenic_linked_strings |= old_node.heterogenic_linked_strings
                
                # старая строка редуцируется к новой
                old_string = old_node.string
                log(f'link {old_string} to {ua}', lvl=5)
                new_node.linked_strings.add(old_string)
                
                # удаляем old_string из prefix_tree
                log(f'rm {old_string} and all its superstrings from prefix trees and table', lvl=3)
                self.rm_bs_from_table_and_trees(old_string, self.table)

                # ну и добавляем в очередь
                self.queue.add(new_qelem)
    
    def normalize_linked_strings(self):
        for node in self.table.values():
            node.linked_strings = set(filter(
                lambda w: self.string_in_one_of_trees(w.prefix()) and self.string_in_one_of_trees(w.suffix()), 
                node.linked_strings
            ))
            node.linked_strings |= node.heterogenic_linked_strings
            node.heterogenic_linked_strings = set()