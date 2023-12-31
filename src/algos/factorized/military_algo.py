from pprint import pp, pformat
from tqdm import tqdm

from monoid import MonoidController, MonoidElem
from universes import Universe
from utils.logger import log, LogFlags

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
        log(lambda: 'MILITARY ALGO STARTED', flags=LogFlags.BRIEF_AND_DET)
        log(lambda: f'sigma is {self.sigma}', lvl=2)
        self.setup()
        self.main_cycle()
        return self.to_sr()

    def to_sr(self):
        return SemigroupRepr(
            self.mc,
            self.table,
            self.value_table,
            set(self.sigma)
        )

    def setup(self):
        log(lambda: 'phase started: SET UP', flags=LogFlags.DETAILED)
        id_node = EasyNode(
            value=self.mc.identity(),
            string=MonoidElem.identity(),
        )
        self.table[MonoidElem.identity()] = id_node
        self.value_table[self.mc.identity()] = id_node
        log(lambda: f'add {id_node.string} -> {id_node.value}', lvl=2)

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
            log(lambda: f'add {new_node.string} -> {new_node.value}', lvl=2)

    def main_cycle(self):
        log(lambda: 'phase started: MAIN CYCLE', flags=LogFlags.DETAILED)

        def generator():
            while len(self.queue) > 0:
                yield

        for _ in tqdm(generator()):
            u_node = self.queue.pop(0)
            u = u_node.string

            for i in self.sigma:
                a = MonoidElem.from_char(i)
                ua = u + a
                # log(lambda: f'{self.table}', lvl=2)
                # log(lambda: f'{self.value_table}', lvl=2)
                log(lambda: f'ua is {ua}', lvl=2)
                log(lambda: f'ua_val is {self.mc.evaluate(ua)}', lvl=2)
                sa = ua.suffix()

                sa_node = self.table.get(sa)

                # sa уже куда-то редуцируется
                if sa_node is None or sa_node.string != sa:
                    log(lambda: f'sa reduces somewhere: just skip', lvl=3)
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
                    log(lambda: f'ua_val is new: create new node', lvl=3)
                    self.table[ua] = new_node
                    self.value_table[ua_val] = new_node
                    self.queue.append(new_node)

                # значение не новое, надо редуцировать
                else:
                    log(lambda: f'ua_val exists: reduce to {min_node.string}', lvl=3) # type: ignore
                    min_node.linked_strings.add(ua)
