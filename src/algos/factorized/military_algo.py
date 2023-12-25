from pprint import pp, pformat
from tqdm import tqdm
import sys

from monoid import MonoidController, MonoidElem
from universes import Universe

from .easy_node import EasyNode
from .semigroup_repr import SemigroupRepr
from .dict_wrapper import DictWrapper
from utils.action_tracker import AT


class MilitaryAlgo:
    mc: MonoidController
    sigma: list[int]
    table: DictWrapper
    value_table: dict[Universe, EasyNode]

    queue: list[EasyNode]

    silence: bool

    def __init__(self, mc: MonoidController,
                 sigma: list[int], silence=True) -> None:
        self.mc = mc
        self.sigma = sigma

        self.table = DictWrapper()
        self.value_table = {}

        self.silence = silence

    def run(self):
        save_stdout = sys.stdout
        if self.silence:
            sys.stdout = open('/dev/null', 'w')

        print('\n>>🦩 Military started')

        self.setup()
        self.main_cycle()

        if self.silence:
            sys.stdout = save_stdout

        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.table,
            self.value_table,
            set(self.sigma)
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

        def generator():
            while len(self.queue) > 0:
                yield

        for _ in tqdm(generator(), disable=self.silence):
            u_node = self.queue.pop(0)
            u = u_node.string

            for i in self.sigma:
                AT.checked_real += 1
                a = MonoidElem.from_char(i)
                ua = u + a

                sa = ua.suffix()

                sa_node = self.table.get(sa)

                # sa уже куда-то редуцируется
                if sa_node is None or sa_node.string != sa:
                    AT.reduced_by_str += 1
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
                    self.value_table[ua_val] = new_node
                    self.queue.append(new_node)
                    AT.new_values_found += 1

                # значение не новое, надо редуцировать
                else:
                    # type: ignore
                    min_node.linked_strings.add(ua)
                    AT.reduced_by_value += 1
