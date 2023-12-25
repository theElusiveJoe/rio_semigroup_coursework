from dataclasses import dataclass, field
from copy import copy

from monoid import MonoidElem
from .easy_node import EasyNode
from utils.action_tracker import AT


class DictWrapper(dict[MonoidElem, EasyNode]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key) -> EasyNode:
        AT.table_lookups += 1
        return super().__getitem__(key)

    def get(self, key) -> EasyNode | None:
        AT.table_lookups += 1
        return super().get(key)
