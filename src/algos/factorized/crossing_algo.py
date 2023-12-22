from __future__ import annotations

from operator import attrgetter
from pprint import pp, pformat
from tqdm import tqdm
from dataclasses import dataclass, field

from universes import Universe
from monoid import MonoidController, MonoidElem
from utils.logger import log, LogFlags
from utils.timer import timer

from .bs_prefix_tree import PrefixTree
from .queue import QueueElem, Queue
from .semigroup_repr import SemigroupRepr
from .easy_node import EasyNode, MonoidElemKind


class DictWrapper(dict[MonoidElem, EasyNode]):
    lookups_counter: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lookups_counter = 0

    def __getitem__(self, key) -> EasyNode:
        self.lookups_counter += 1
        return super().__getitem__(key)

    def get(self, key) -> EasyNode | None:
        self.lookups_counter += 1
        return super().get(key)


@dataclass
class ActionTracker:
    expect_to_check: int = field(default=0)
    checked_real: int = field(default=0)
    skipped_as_bs: int = field(default=0)
    reduced_by_str: int = field(default=0)
    reduced_by_value: int = field(default=0)
    replaced_old_strings: int = field(default=0)
    new_values_found: int = field(default=0)


class CrossingAlgo:
    mc: MonoidController
    table: DictWrapper
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

    def string_in_one_of_trees(self, string: MonoidElem):
        return bool(self.bs_A.find_node(string) or self.bs_B.find_node(string))

    def run(self):
        log(lambda: 'CROSSING ALGO STARTED', flags=LogFlags.BRIEF_AND_DET)

        self.grow_bs_prefix_tree()
        self.merge_cayley_graphs()
        self.setup_queue()
        self.calc_crossing()
        self.normalize_linked_strings()

        log(lambda: 'CROSSING ALGO FINISHED', flags=LogFlags.DETAILED)

        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            dict(self.table),
            self.value_table,
            self.sr1.sigma | self.sr2.sigma
        )

    def grow_bs_prefix_tree(self):
        # строим дерево базовых строк
        log(lambda: 'phase started: TREE GROWING', flags=LogFlags.DETAILED)

        self.bs_A = PrefixTree(
            bs=[(node.string, val)
                for val, node in sorted(self.sr1.value_table.items(), key=lambda pair: pair[1].string)
                if val != self.mc.identity()],
            id_val=self.mc.identity(),
        )
        self.bs_B = PrefixTree(
            bs=[(node.string, val)
                for val, node in sorted(self.sr2.value_table.items(), key=lambda pair: pair[1].string)
                if val != self.mc.identity()],
            id_val=self.mc.identity(),
        )

    def rm_bs_from_table_and_trees(self, string: MonoidElem, table: dict):
        self.bs_A.delete_all_superstrings_from_table_and_tree(string, table)
        self.bs_B.delete_all_superstrings_from_table_and_tree(string, table)

    def merge_cayley_graphs(self):
        values1, values2 = set(self.sr1.value_table.keys()), set(
            self.sr2.value_table.keys())
        # values1.discard(self.mc.identity())
        # values2.discard(self.mc.identity())
        common_values = values1.intersection(values2)

        log(lambda: f'values A: {values1}', lvl=2)
        log(lambda: f'values B: {values2}', lvl=2)
        log(lambda: f'values COMMON: {common_values}', lvl=2)

        log(lambda: 'phase started: MERGE', flags=LogFlags.DETAILED)
        for cv in common_values:
            log(lambda: f'cv: {cv}', lvl=2)
            n1, n2 = self.sr1.value_table[cv], self.sr2.value_table[cv]
            log(lambda: f'node1: {n1}', lvl=3)
            log(lambda: f'node2: {n2}', lvl=3)
            log(lambda: f'node1 {"<" if n1.string < n2.string else ">"} node2', lvl=3)

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
            log(lambda: f'link {node.string} to {short_node.string}', lvl=3)
            if not short_node.string.is_identity():
                short_node.linked_strings.add(node.string)
            log(lambda: f'link {node.linked_strings} to {short_node.string}', lvl=3)
            short_node.linked_strings |= node.linked_strings

            # удаляем node.string из prefix_tree
            log(lambda: f'rm {node.string} and all its superstrings from prefix trees and table', lvl=3)
            self.rm_bs_from_table_and_trees(node.string, table)
            tree_with_big_string.delete_all_superstrings_from_table_and_tree(
                node.string, table)

        # соберем вместе две таблицы
        self.table = DictWrapper({**self.sr1.table, **self.sr2.table})
        self.value_table = {**self.sr1.value_table, **self.sr2.value_table}

    def setup_queue(self):
        log(lambda: 'phase started: QUEUE SET UP', flags=LogFlags.DETAILED)
        self.queue = Queue()

        q = list[QueueElem]()

        for bs_node in self.bs_A.root.get_succ_nodes():
            q.append(
                QueueElem(
                    prefix=MonoidElem.identity(),
                    prefix_value=self.mc.identity(),
                    bs_node=bs_node,
                    kind=MonoidElemKind.A,
                )
            )

        for bs_node in self.bs_B.root.get_succ_nodes():
            q.append(
                QueueElem(
                    prefix=MonoidElem.identity(),
                    prefix_value=self.mc.identity(),
                    bs_node=bs_node,
                    kind=MonoidElemKind.B,
                )
            )

        for qelem in sorted(q, key=lambda x: x.bs_node.string.last()):
            self.queue.add(qelem)

        log(lambda: f'now queue is {self.queue}', lvl=2)

    def calc_crossing(self):
        log(lambda: 'phase started: CROSSING', flags=LogFlags.DETAILED)
        at = ActionTracker()

        def generator():
            while len(self.queue) > 0:
                yield

        for _ in tqdm(generator()):
            # выдергиваем следующий из очереди
            log(lambda: f'now queue is {self.queue}', lvl=2)
            qelem = self.queue.pop()
            log(lambda: f'u = {qelem}', lvl=2)

            # конструируем множества следующих строк
            # нужно только для лога
            switch_kind_nodes = self.another_bs_kind(
                qelem.kind).root.get_succ_nodes()
            succ_nodes = qelem.bs_node.get_succ_nodes()
            log(lambda: 
                f'switch kind variants: {list(map(attrgetter("string"), switch_kind_nodes))}',
                lvl=3)
            log(lambda: 
                f'succ nodes variants: {list(map(attrgetter("string"), succ_nodes))}',
                lvl=3)
            at.expect_to_check += len(switch_kind_nodes) + len(succ_nodes)

            def next_switch_kind():
                log(lambda: 'this is switch kind', lvl=4)
                return QueueElem(
                    qelem.to_string(),
                    qelem.prefix_value * qelem.bs_node.value,
                    sk_node,  # type: ignore
                    qelem.kind.another(),
                )

            def next_succ():
                log(lambda: 'this is next succ', lvl=4)
                return QueueElem(
                    qelem.prefix,
                    qelem.prefix_value,
                    succ_node,  # type: ignore
                    qelem.kind,
                )

            log(lambda: 'iterate succ and switch_kind', lvl=3)

            # узлы, из которых растут новые постфиксы
            sk_root, succ_root = self.another_bs_kind(
                qelem.kind).root, qelem.bs_node
            # все потенциальные новые префиксы
            sk_keys, succ_keys = sk_root.get_succ_keys(), succ_root.get_succ_keys()
            sk_index, succ_index = 0, 0

            # перебераем все следующие строки
            while True:
                try:
                    sk_node = sk_root.get_succ(sk_keys[sk_index])
                    while sk_node is None:
                        sk_index += 1
                        sk_node = sk_root.get_succ(sk_keys[sk_index])
                except IndexError:
                    sk_node = None

                try:
                    succ_node = succ_root.get_succ(succ_keys[succ_index])
                    while succ_node is None:
                        succ_index += 1
                        succ_node = succ_root.get_succ(succ_keys[succ_index])
                except IndexError:
                    succ_node = None

                if sk_node is None and succ_node is None:
                    break
                elif succ_node is None or sk_node is not None and sk_node.string.last() < succ_node.string.last():
                    new_qelem = next_switch_kind()
                    sk_index += 1
                else:
                    new_qelem = next_succ()
                    succ_index += 1

                log(lambda: f'ua = {new_qelem}', lvl=5)
                at.checked_real += 1

                # ua - это базовая строка - т.е. prefix = eps
                # ua только что вышел из prefix tree,
                # значит sa точно никуда не редуцируется
                # и есть в таблицах
                # просто добавим ее в очередь
                if new_qelem.prefix.is_identity():
                    self.queue.add(new_qelem)
                    log(lambda: 'new_qelem in basic strings: just add it to queue', lvl=5)
                    at.skipped_as_bs += 1
                    continue

                ua = new_qelem.to_string()
                sa = ua.suffix()
                sa_node = self.table.get(sa)

                # sa редуцируема, если ее нет в таблице
                if sa_node is None:
                    log(lambda: 'new_qelem in is reducable: skip', lvl=5)
                    at.reduced_by_str += 1
                    continue

                log(lambda: f'sa is {sa} and it is not reducable!', lvl=5)

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
                    log(lambda: 'new_qelem_val is new: add to queue', lvl=5)
                    at.new_values_found += 1
                    continue

                # такое значение есть, и эта строка не превосходит уже
                # найденную
                if ua_min_node.string < ua:
                    log(lambda: 
                        f'string with such value exists {ua_min_node.string} and less than ua: just link ua to it', lvl=5) # type: ignore
                    ua_min_node.heterogenic_linked_strings.add(ua)
                    at.reduced_by_value += 1
                    continue
                # такое значение есть,
                # ua < ua_min_string
                # значит, ua_min_string - гомогенная
                else:
                    old_node = ua_min_node
                    log(lambda: 
                        f'string with such value exists {old_node.string}, but ua {ua} is less', lvl=5)
                    # создаем новый узел
                    new_node = EasyNode(
                        value=ua_val,
                        string=ua,
                    )

                    # записываем новый узел в таблицы
                    self.table[ua] = new_node
                    self.value_table[ua_val] = new_node

                    log(lambda: f'link {old_node.linked_strings} and {old_node.heterogenic_linked_strings} to {ua}', lvl=5)
                    new_node.linked_strings |= old_node.linked_strings
                    new_node.heterogenic_linked_strings |= old_node.heterogenic_linked_strings

                    # старая строка редуцируется к новой
                    old_string = old_node.string
                    log(lambda: f'link {old_string} to {ua}', lvl=5)
                    new_node.linked_strings.add(old_string)

                    # удаляем old_string из prefix_tree
                    log(lambda: f'rm {old_string} and all its superstrings from prefix trees and table', lvl=5)
                    self.rm_bs_from_table_and_trees(old_string, self.table)

                    # ну и добавляем в очередь
                    log(lambda: f'add {new_qelem} to queue', lvl=5)
                    self.queue.add(new_qelem)
                    at.replaced_old_strings += 1

        log(lambda: f'total table lookups: {self.table.lookups_counter}',
            lvl=2, flags=LogFlags.BRIEF_AND_DET)
        pp(at)

    def normalize_linked_strings(self):
        log(lambda: 'phase started: LINKED STRINGS NORMALIZATION', flags=LogFlags.DETAILED)

        for node in self.table.values():
            node.linked_strings = set(filter(
                lambda w: self.string_in_one_of_trees(
                    w.prefix()) and self.string_in_one_of_trees(w.suffix()),
                node.linked_strings
            ))
            node.linked_strings |= node.heterogenic_linked_strings
            node.heterogenic_linked_strings = set()
