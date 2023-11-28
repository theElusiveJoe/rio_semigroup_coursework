from universes.abstract import Universe


class Test:
    generators: list[Universe]
    names: list[str] | None

    def __init__(self, universe_type: type[Universe], *generators) -> None:
        self.generators = [universe_type(g) for g in generators]
        self.names = [chr(i+97) for i in range(len(self.generators))]
