from .order_config import OrderConfig
from .logger import Logger
from universes.abstract import Universe
from monoid import MonoidController, MonoidElem, RulesSystem


class Algo:
    mc: MonoidController
    k: int
    rules: RulesSystem

    frontier: list[MonoidElem]
    min_base_val: dict[MonoidElem, Universe]
    min_val_base: dict[Universe, MonoidElem]

    order_cfg: OrderConfig
    logger: Logger

    def __init__(self,
                 mc: MonoidController,
                 order_cfg: OrderConfig
                 ) -> None:
        self.mc = mc
        self.k = len(self.mc.generators)
        self.rules = RulesSystem(mc=self.mc)

        self.frontier = []
        self.min_base_val = dict()
        self.min_val_base = dict()

        self.order_cfg = order_cfg
        self.logger = Logger()

    @staticmethod
    def log(lvl=1, str=''):
        print('    ' * (lvl - 1) + '' + str)

    def add_to_frontier(self, s: MonoidElem):
        new_elems = [s + MonoidElem.from_char(i) for i in range(self.k)]
        self.order_cfg.add_func(self.frontier, new_elems)

    def frontier_is_empty(self):
        return len(self.frontier) == 0

    def get_from_frontier(self):
        assert not self.frontier_is_empty()
        felem = self.order_cfg.pop_func(self.frontier)
        self.logger.frontier_seq.append(felem)
        return felem

    def upd_base_val(self, base: MonoidElem, val: Universe):
        self.min_val_base[val] = base
        self.min_base_val[base] = val

    def look_up_val(self, elem: MonoidElem) -> Universe:
        self.logger.val_lookups += 1
        return self.min_base_val[elem]

    def look_up_base(self, elem: Universe) -> MonoidElem | None:
        self.logger.base_lookups = + 1
        return self.min_val_base.get(elem)

    def set_up(self):
        self.add_to_frontier(MonoidElem.identity())
        self.upd_base_val(MonoidElem.identity(), self.mc.identity())

    def main_cycle(self):
        while not self.frontier_is_empty():
            u = self.get_from_frontier()
            self.log(1, f'u = {self.mc.to_string(u)}')

            w = u.prefix()
            a = u.last()

            w_val = self.look_up_val(w)
            a_val = self.mc.evaluate(a)
            u_val = w_val * a_val

            self.log(2, f'u val =  {u_val}')
            # такое значение уже есть
            u_min = self.look_up_base(u_val)
            if u_min is not None and isinstance(u_min, MonoidElem):
                self.log(2, f'u val is not new')
                self.rules.add_rule(u, u_min)
            # мы встретили новое значение
            else:
                self.log(2, f'u val is new')
                self.add_to_frontier(u)
                self.upd_base_val(u, u_val)

    def run(self):
        self.set_up()
        self.main_cycle()
        return self.rules
