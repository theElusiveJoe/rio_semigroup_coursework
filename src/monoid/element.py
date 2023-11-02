from __future__ import annotations
from typing import Iterable


class MonoidElem:
    symbols: list[int] 

    def __init__(self, seq: Iterable[int]) -> None:
        self.symbols = list(seq)

    def __len__(self):
        return len(self.symbols)
    
    def __getitem__(self, i: int) -> int:
        return self.symbols[i]
    
    def __repr__(self):
        return '(' + ','.join(map(str,self.symbols)) + ')'
    
    def __add__(self, other:MonoidElem):
        return MonoidElem(self.symbols + other.symbols)
    
    def __eq__(self, other: MonoidElem) -> bool:
        assert type(other) == MonoidElem
        return self.symbols == other.symbols
    
    def __hash__(self) -> int:
        return 0 if not self.symbols else self.symbols[-1]
    
    def __contains__(self, other):
        for i in range(len(self)):
            if other.symbols == self.symbols[i:i+len(other)]:
                return True
        return False
    
    def first(self):
        return MonoidElem([self[0]])
    
    def last(self):
        return MonoidElem([self[-1]])
    
    def prefix(self):
        return MonoidElem(self.symbols[:-1])
    
    def suffix(self):
        return MonoidElem(self.symbols[1:])
    
    @staticmethod
    def from_char(char:int) -> MonoidElem:
        return MonoidElem([char])
    
    @staticmethod
    def identity() -> MonoidElem:
        return MonoidElem([])
    
    def is_identity(self):
        return len(self) == 0
    
    def letter(self):
        assert len(self) == 1
        return self[0]