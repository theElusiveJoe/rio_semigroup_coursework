from typing import NamedTuple, Callable
from monoid import MonoidElem


class OrderConfig(NamedTuple):
    add_func: Callable[[list[MonoidElem], list[MonoidElem]], None]
    pop_func: Callable[[list[MonoidElem]], MonoidElem]
    desc: str = ''
