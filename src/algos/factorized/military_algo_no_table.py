from monoid import MonoidController, MonoidElem
from universes import Universe
from ....misc.easy_node_no_table import EasyNode
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

        self.table = dict()
        self.value_table = dict()

        self.queue = []

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.sigma,
            self.table,
            self.value_table
        )

    def run(self):
        self.setup()
        self.main_cycle()
        return self.to_sr

    def setup(self):
        id_node = EasyNode(
            value=self.mc.identity(),
            first=MonoidElem.identity(),
            last=MonoidElem.identity(),
            prefix=None,  # type: ignore
            suffix=None,  # type: ignore
            len=0,
        )
        id_node.prefix = id_node.suffix = id_node
        self.table[MonoidElem.identity()] = id_node
        self.value_table[self.mc.identity()] = id_node

        for i in self.sigma:
            a = MonoidElem.from_char(i)
            a_val = self.mc.generators[i]
            new_node = EasyNode(
                value=a_val,
                first=a,
                last=a,
                prefix=id_node,
                suffix=id_node,
                len=1,
            )
            self.table[a] = new_node
            self.value_table[a_val] = new_node
            self.queue.append(new_node)

            id_node.pau[i] = id_node.pua[i] = new_node

    def main_cycle(self):
        while len(self.queue) != 0:
            u_node = self.queue.pop(0)
            s_node = u_node.suffix

            for i in self.sigma:
                sa_node = s_node.pua.get(i)

                # sa уже куда-то редуцируется
                if sa_node is None:
                    continue

                # вычисляем значение
                ua_val = u_node.value * self.mc.generators[i]
                # ищем ноду с таким же значением
                min_node = self.value_table.get(ua_val)

                # ноды нет, значит значение новое
                if min_node is None:
                    new_node = EasyNode(
                        value=ua_val,
                        first=u_node.first,
                        last=MonoidElem.from_char(i),
                        prefix=u_node,
                        suffix=sa_node,
                        len=u_node.len+1
                    )

                    u_node.pau[i] = new_node
                    sa_node.pua[u_node.first.letter()] = new_node
                    self.queue.append(new_node)
                    continue

                # значение не новое, надо редуцировать
                ua = u_node.retrieve_string() + MonoidElem.from_char(i)
                min_node.linked_strings.add(ua)
