from monoid import MonoidController, MonoidElem
from universes import Universe

from .easy_node import EasyNode
from .semigroup_repr import SemigroupRepr


class MilitaryAlgo:
    mc: MonoidController
    sigma: list[int]
    table: dict[MonoidElem, EasyNode]
    value_table: dict[Universe, EasyNode]

    queue: list[EasyNode]

    def __init__(self, mc: MonoidController, sigma: list[int]) -> None:
        self.mc = mc
        self.sigma = sigma

        self.table = {}
        self.value_table = {}

    def run(self):
        self.setup()
        self.main_cycle()
        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.table,
            self.value_table
        )

    def setup(self):
        id_node = EasyNode(
            value=self.mc.identity(),
            string=MonoidElem.identity(),
        )
        self.table[MonoidElem.identity()] = id_node
        self.value_table[self.mc.identity()] = id_node

        self.queue = []
        for i in self.sigma:
            a = MonoidElem.from_char(i)
            a_val = self.mc.generators[i]
            new_node = EasyNode(
                value=a_val,
                string=a,
            )
            self.table[a] = new_node
            self.value_table[a_val] = new_node
            self.queue.append(new_node)

    def main_cycle(self):
        while len(self.queue) != 0:
            u_node = self.queue.pop(0)
            u = u_node.string

            for i in self.sigma:
                a = MonoidElem.from_char(i)
                ua = u+a
                sa = ua.suffix()

                sa_node = self.table.get(sa)

                # sa уже куда-то редуцируется
                if sa_node is None or sa_node.string != sa:
                    continue

                # вычисляем значение
                ua_val = u_node.value * self.mc.generators[i]
                # ищем ноду с таким же значением
                min_node = self.value_table.get(ua_val)

                # ноды нет, значит значение новое
                if min_node is None:
                    new_node = EasyNode(
                        value=ua_val,
                        string=ua
                    )
                    self.table[ua] = new_node
                    self.queue.append(new_node)

                # значение не новое, надо редуцировать
                else:
                    self.table[ua] = min_node
                    min_node.linked_strings.add(ua)

                # запоминаем, что есть надстрока в таблице
                u_node.pua.add(i)
                sa_node.pau.add(u.first().letter())
