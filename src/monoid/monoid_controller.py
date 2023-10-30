from universes.abc_universe import Universe
from monoid.monoid_elem import MonoidElem


class MonoidController:
    universe_type: type
    generating: list[Universe]
    symbols: list[str]

    def __init__(self, seq: list[Universe], names: list[str]) -> None:
        self.universe_type = type(seq[0])

        e = seq[0].e()
        seq = [x for x in seq if x != e]
        seq = seq

        self.generating = seq
        self.symbols = names

        print(f'generating: {self.generating}')
        assert len(self.generating) == len(self.symbols)

    def get_e(self):
        return self.generating[0].e()

    def compare(self, e1: MonoidElem, e2: MonoidElem) -> int:
        '''
        1 if e1 > e2 
        0 if e1 == e2
        -1 else
        '''

        if len(e1) > len(e2):
            return 1
        if len(e1) < len(e2):
            return -1
        
        if e1.symbols > e2.symbols:
            return 1
        if e1.symbols < e2.symbols:
            return -1    
        
        return 0
    
    def evaluate(self, e: MonoidElem):
        if e == MonoidElem([-1]):
            return self.get_e()
        elems = [self.generating[i] for i in e.symbols]

        res = elems[0]
        for x in elems[1:]:
            res = res*x

        return res
    
    def next(self, elem: MonoidElem):
        if elem == MonoidElem([-1]):
            return MonoidElem([self.generating[0]])
        seq = elem.symbols

        base = len(self.symbols)
        num = 0
        for i in seq:
            num *= base 
            num += i
        num += 1

        new_seq = []
        while num:
            new_seq.insert(0, num%base)
            num = num // base

        return MonoidElem(new_seq)
    
    def to_names(self, e: MonoidElem):
        return [self.symbols[i] for i in e.symbols]
    
    def from_names(self, syms: list[str]):
        idxs = [self.symbols.index(s) for s in syms]
        return MonoidElem(idxs)
                


