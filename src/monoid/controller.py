from universes.abstract import Universe
from monoid.element import MonoidElem


class MonoidController:
    universe_type: type
    generators: list[Universe]
    names: list[str]

    def __init__(self, seq: list[Universe]) -> None:
        self.universe_type = type(seq[0])

        if seq[0].identity() in seq:
            raise RuntimeError(f'identity elem can not be generator')

        self.generators = seq
        self.names = [chr(i) for i in range(
            ord('a'), ord('a') + len(self.generators))]

    def identity(self) -> Universe:
        return self.generators[0].identity()
