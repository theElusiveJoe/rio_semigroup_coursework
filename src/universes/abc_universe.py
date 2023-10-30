from __future__ import annotations
from abc import ABC, abstractmethod


class Universe(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __mul__(self, o):
        pass

    @abstractmethod
    def __eq__(self, o):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def e() -> Universe:
        pass

