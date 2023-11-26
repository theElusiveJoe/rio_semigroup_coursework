from monoid import MonoidController, MonoidElem, RulesSystem


class Logger:
    frontier_seq: list[MonoidElem] = []
    val_lookups: int = 0
    base_lookups: int = 0
    universe_evals: int = 0
