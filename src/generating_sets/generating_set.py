
from dataclasses import dataclass
from universes.abstract import Universe
from monoid import MonoidController


@dataclass
class GeneratingSet:
    mc: MonoidController
    sigma: list[int]

    @staticmethod
    def build_from_description(universe_type: type[Universe], *generators_desc):
        generators = [universe_type(g) for g in generators_desc]
        return GeneratingSet(
            mc=MonoidController(generators),
            sigma=[i for i in range(len(generators))]

        )