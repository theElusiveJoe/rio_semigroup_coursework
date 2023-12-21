from universes.abstract import Universe
from monoid import MonoidController


class GeneratingSet:
    mc: MonoidController
    sigma: list[int]

    def __init__(self, mc: MonoidController,
                 sigma: list[int], check_duplicates: bool = True):
        self.mc = mc
        if check_duplicates:
            # фильтруем повторяющиеся значения
            generators = [self.mc.generators[i] for i in sigma]
            filtered_sigma = []
            for i in sigma:
                if self.mc.generators[i] in generators[:i]:
                    continue
                filtered_sigma.append(i)
            self.sigma = filtered_sigma
        else:
            self.sigma = sigma

    @staticmethod
    def build_from_description(
            universe_type: type[Universe], *generators_desc):
        generators = [universe_type(g) for g in generators_desc]
        id_elem = generators[0].identity()
        generators = list(filter(lambda x: x != id_elem, generators))
        return GeneratingSet(
            mc=MonoidController(generators),
            sigma=[i for i in range(len(generators))]
        )

    def to_mc_and_sigma(self):
        return self.mc, self.sigma
