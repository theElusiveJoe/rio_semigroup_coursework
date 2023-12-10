from __future__ import annotations
from abc import ABC, abstractmethod


class Universe(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __mul__(self, o) -> Universe:
        pass

    @abstractmethod
    def __eq__(self, o) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def identity(self) -> Universe:
        pass
