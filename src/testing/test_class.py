from typing import Any
from universes.abstract import Universe
from monoid.controller import MonoidController
from algos.extended import Algo



class Test:
    generators: list[Universe]
    names: list[str]|None

    def __init__(self, universe_type: type[Universe], *generators) -> None:
        self.generators = [universe_type(g) for g in generators]
        if len(self.generators) <= 26:  
            self.names = [chr(i+97) for i in range(len(self.generators))]
        else:
            self.names = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run()

    def run(self):
        mc = MonoidController(self.generators, self.names)
        algo = Algo(mc)
        algo.run()

        print(algo.rules)
        return algo
        
