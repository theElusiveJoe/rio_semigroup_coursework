from universes.abstract import Universe
from monoid.controller import MonoidController
from monoid.element import MonoidElem


class Algo:
    contoller: MonoidController

    def __init__(self, mc: MonoidController) -> None:
        self.contoller = mc

    def __len__(self):
        return len(self.queue)

    def next(self):
        u = self.queue[0]
        self.queue = self.queue[1:]
        return u

    def run(self):
        self.queue = [MonoidElem([i])
                      for i in range(len(self.contoller.generators))]
        known_elems = dict()
        for elem in self.queue:
            known_elems[self.contoller.evaluate(elem)] = elem
        u = self.next()

        rules = []
        while True:
            print(f'-> u =', u)
            for ai in range(len(self.contoller.generators)):
                uai = u + MonoidElem([ai])
                uai_val = self.contoller.evaluate(uai)
                print(f'->     uai = ({uai})', end='; ')
                print(f'uai_val = {uai_val}')
                if uai_val not in known_elems:
                    print(f'->     uai is new elem!')
                    known_elems[uai_val] = uai
                    self.queue.append(uai)
                else:
                    print(f'->     uai is already known!')
                    rules.append((
                        uai,
                        known_elems[uai_val]
                    ))

            if len(self) > 0:
                u = self.next()
            else:
                break

        return rules
