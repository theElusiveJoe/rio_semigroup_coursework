import itertools
from numpy import cumsum
from universes.abstract import Universe
from monoid import MonoidController

from .generating_set import GeneratingSet


class GeneratingSetsFamily:
    mc: MonoidController
    sigmas: list[list[int]]

    def __init__(self, mc: MonoidController, sigmas: list[list[int]]):
        self.mc = mc
        # фильтруем повторяющиеся значения
        seen_values = set()
        filtered_sigmas_list = []
        for sigma_list in sigmas:
            filtered_sigma = []
            for sigma in sigma_list:
                if self.mc.generators[sigma] in seen_values:
                    continue
                filtered_sigma.append(sigma)
                seen_values.add(self.mc.generators[sigma])
            filtered_sigmas_list.append(filtered_sigma)
        self.sigmas = filtered_sigmas_list

    def __len__(self):
        return len(self.sigmas)

    @staticmethod
    def build_from_description(
            universe_type: type[Universe], *generators_desc: list):
        generators = [
            [universe_type(g) for g in gl]
            for gl in generators_desc
        ]
        identity = generators[0][0].identity()
        generators = [
            list(filter(lambda x: x != identity, gl))
            for gl in generators
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
            list(itertools.chain(*self.sigmas)),
            check_duplicates=False
        )

    def get_generating_set(self, i: int):
        return GeneratingSet(
            mc=self.mc,
            sigma=self.sigmas[i],
            check_duplicates=False
        )

    def get_all_generating_sets(self):
        return [self.get_generating_set(i) for i in range(len(self))]
