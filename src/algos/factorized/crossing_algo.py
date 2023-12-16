from __future__ import annotations

from operator import attrgetter
from pprint import pp

from universes import Universe
from monoid import MonoidController, MonoidElem
from utils import log 

from .bs_prefix_tree import PrefixTree, PrefixTreeNode
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

    def run(self):
        log('CROSSING ALGO')
        self.merge_cayley_graphs()
        self.grow_bs_prefix_tree()
        self.setup_queue()
        self.calc_crossing()
        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.table,
            self.value_table
        )

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
            table, value_table, node, short_node = (
                (self.sr2.table, self.sr2.value_table, n2, n1)
                if n1.string < n2.string
                else (self.sr1.table, self.sr1.value_table, n1, n2)
            )

            # убираем ноду из  таблицы значений
            del value_table[cv]
            table[node.string] = short_node
            log(f'link {node.string} to {short_node.string}', lvl=3)

            # заменяем правила редукции
            for ls in node.linked_strings:
                table[ls] = short_node
                short_node.linked_strings.add(ls)
            log(f'link {node.linked_strings} to {short_node.string}', lvl=3)

        # соберем вместе две таблицы
        self.table = {**self.sr1.table, **self.sr2.table}
        self.value_table = {**self.sr1.value_table, **self.sr2.value_table}

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
        log(f'now queue is {self.queue}')

    def calc_crossing(self):
        log('CROSSING STARTED')
        while len(self.queue) > 0:
            # выдергиваем следующий из очереди
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

            switch_kind_nodes = self.another_bs_kind(
                qelem.kind).root.succ.values()
            succ_nodes = qelem.bs_node.succ.values()
            log(f'switch kind variants: {list(map(attrgetter("string"), switch_kind_nodes))}', lvl=3)
            log(f'succ nodes variants: {list(map(attrgetter("string"), succ_nodes))}', lvl=3)
            sk_index, sn_index = 0, 0

            def next_switch_kind():
                log('this is switch kind', lvl=4)
                return QueueElem(
                    qelem.to_string() ,
                    qelem.prefix_value * qelem.bs_node.value,
                    switch_kind_nodes[sk_index],  # type: ignore
                    qelem.kind.another(),
                )

            def next_succ():
                log('this is next succ', lvl=4)
                return QueueElem(
                    qelem.to_string(),
                    qelem.prefix_value,
                    succ_nodes.get[sn_index],
                    qelem.kind,
                )

            log('iterate succ and switch_kind', lvl=3)
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
                log(f'ua = {new_qelem}', lvl=5)
                if new_qelem.prefix.is_identity():
                    raise RuntimeError('never executes!')
                    self.queue.add(new_qelem)
                    log('new_qelem in basic strings: just add it to queue', lvl=5)
                    continue

                ua = new_qelem.to_string()
                sa = ua.suffix()
                sa_node = self.table.get(sa)

                # sa сократима, если ее нет в таблице, или она редуцируется
                if sa_node is None or sa_node.string != sa:
                    log('new_qelem in is reducable: skip', lvl=5)
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
                    log('new_qelem_val is new: add to queue', lvl=5)
                    continue

                # такое значение есть, и эта строка не превосходит уже найденную
                if ua_min_node.string < ua:
                    self.table[ua] = ua_min_node
                    ua_min_node.linked_strings.add(ua)
                    log(f'string with such value exists {ua_min_node.string} and less than ua: just link ua to it', lvl=5)
                    continue

                # такое значение есть, но оно меньше уже найденного
                old_node = ua_min_node
                log(f'string with such value exists {old_node.string}, but ua is less', lvl=5)
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
                log(f'link {old_node.string} to {ua}', lvl=5)
                # и все строки, которые к ней редуцировались - тоже
                for ls in old_node.linked_strings:
                    self.table[ls] = new_node
                log(f'link {old_node.linked_strings} to {ua}', lvl=5)
                # если старый узел содержал базовую строку,
                # то эту базовую строку надо удалить из bs_tree,
                # чтобы больше не использовать ни эту строку, ни ее потомков
                self.bs_A.delete(old_node.string)
                self.bs_B.delete(old_node.string)

                # ну и добавляем в очередь
                self.queue.add(new_qelem)


