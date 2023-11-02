from universes.abstract import Universe
from monoid.element import MonoidElem


class MonoidController:
    universe_type: type
    generators: list[Universe]
    names: list[str]|None

    def __init__(self, seq: list[Universe], names: list[str]|None = None) -> None:
        self.universe_type = type(seq[0])

        if seq[0].identity() in seq:
            raise RuntimeError(f'identity elem can not be generator')

        self.generators = seq
        self.names = names

    def identity(self):
        return self.generators[0].identity()

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
        if e.is_identity:
            return self.identity
        elems = [self.generators[i] for i in e.symbols]

        res = elems[0]
        for x in elems[1:]:
            res = res*x

        return res

    def to_names(self, e: MonoidElem):
        if self.names is None:
            return map(str, e.symbols)
        return [self.names[i] for i in e.symbols]
    
    def to_string(self, e: MonoidElem):
        if e.is_identity():
            return 'eps'
        if self.names is None:
            return ','.join(map(str, e.symbols))
        return ''.join(self.to_names(e))
    
    def next(self, elem: MonoidElem):
        def loop(seq):
            if seq == []:
                return [0]
            if seq[-1] == len(self.generators)-1:
                return loop(seq[:-1]) + [0]
            return seq[:-1] + [seq[-1]+1]
                
        ret =  MonoidElem(loop(elem.symbols))
        return ret

