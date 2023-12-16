import itertools
from dataclasses import dataclass
from numpy import cumsum
from universes.abstract import Universe
from monoid import MonoidController

from .generating_set import GeneratingSet


@dataclass
class GeneratingSetsFamily:
    mc: MonoidController
    sigmas: list[list[int]]

    def __len__(self):
        return len(self.sigmas)

    @staticmethod
    def build_from_description(universe_type: type[Universe], *generators_desc: tuple[list]):
        generators = [
            [universe_type(g) for g in gl]
            for gl in generators_desc
        ]
        mc = MonoidController(list(itertools.chain(*generators)))
        lens_cs = cumsum(list(map(len, generators))).tolist()
        sigmas = [
            [i + len_pre for i in range(len(cur_list))]
            for len_pre, cur_list in zip([0] + lens_cs, generators)
        ]
        return GeneratingSetsFamily(
            mc=mc,
            sigmas=sigmas
        )

    def to_one_generating_set(self):
        return GeneratingSet(
            self.mc,
            list(itertools.chain(*self.sigmas))
        )

    def get_generating_set(self, i: int):
        return GeneratingSet(
            mc=self.mc,
            sigma=self.sigmas[i]
        )
