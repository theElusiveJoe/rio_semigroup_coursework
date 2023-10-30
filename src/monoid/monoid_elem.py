from __future__ import annotations
from copy import deepcopy


class MonoidElem:
    symbols: list[int] 

    def __init__(self, seq) -> None:
        self.symbols = seq

    def __len__(self):
        return len(self.symbols)
    
    def __getitem__(self, i: int) -> int:
        return self.symbols[i]
    
    def __repr__(self):
        return ','.join(map(str,self.symbols))
    
    def __add__(self, other:MonoidElem):
        return MonoidElem(deepcopy(self.symbols) + deepcopy(other.symbols))
    
    def __eq__(self, other: MonoidElem) -> bool:
        return self.symbols == other.symbols
    
    def __hash__(self) -> int:
        return self.symbols[-1]
    
    def simplify(self, rules:list[tuple[MonoidElem, MonoidElem]]):
        for i in range(len(self)):
            for a, b in rules:
                a,b = a.symbols, b.symbols
                la = len(a)
                if tuple(self.symbols[i: i+la]) == a:
                    return MonoidElem(
                        deepcopy(self.symbols[:i]) +
                        list(deepcopy(b)) + 
                        deepcopy(self.symbols[i+la:])   
                    ).simplify(rules)
                
        return self
                
