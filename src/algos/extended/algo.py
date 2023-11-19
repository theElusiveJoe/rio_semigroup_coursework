from universes.abstract import Universe
from monoid.controller import MonoidController
from monoid.element import MonoidElem
from algos.extended.node import ExtendedNode
from monoid.rules import RulesSystem


class ExtendedAlgo:
    mc: MonoidController
    k: int
    rules: RulesSystem
    table: dict[MonoidElem, ExtendedNode]

    def __init__(self, mc: MonoidController) -> None:
        self.mc = mc
        self.k = len(self.mc.generators)
        self.rules = RulesSystem(mc=self.mc)
        self.table = dict()

    @staticmethod
    def log(lvl=1, str=''):
        print('    '*(lvl-1) + '' + str)

    def draw_table(self):
        print('Table:')
        for k, v in self.table.items():
            print(f'    {self.mc.to_string(k)} -> ' +
                  f'{self.mc.to_string(v.retrieve_string())}: {v.value}')

    def run(self):
        self.init_identity_and_generators()
        self.main_cycle()
        return self.rules

    def init_identity_and_generators(self):
        identity_node = ExtendedNode(
            value=self.mc.identity(),
            first=MonoidElem.identity(),
            last=MonoidElem.identity(),
            prefix=MonoidElem.identity(),
            suffix=MonoidElem.identity(),
            len=0,
            next=MonoidElem.from_char(0),
        )
        self.table[MonoidElem.identity()] = identity_node

        for i in range(self.k):
            self.table[MonoidElem.from_char(i)] = ExtendedNode(
                value=self.mc.generators[i],
                first=MonoidElem.from_char(i),
                last=MonoidElem.from_char(i),
                prefix=MonoidElem.identity(),
                suffix=MonoidElem.identity(),
                len=1,
                next=MonoidElem.from_char(i+1)
                if i < self.k-1 else MonoidElem.identity()
            )

            identity_node.pau.append(MonoidElem.from_char(i))
            identity_node.pua.append(MonoidElem.from_char(i))
            identity_node.pua_flag.append(True)

    def main_cycle(self):
        cur_len = 1
        # u is current string
        # we calculate ua for each a in generators
        u = MonoidElem([0])
        # v is smallest string of current length
        v = u
        # last is the greatest irreducable string we met 
        last = MonoidElem([self.k-1])
        # by default we set identity elem as next for each new node
        # the algorithm converged, when u.next is identity (u if the greatest string)
        while u != MonoidElem.identity():

            self.log(1, f'computing uai for each u of length {cur_len}')
            # actually, we dont need this assertion
            assert len(v) == cur_len

            while len(u) == cur_len:
                self.log(2, f'u = {self.mc.to_string(u)}')
                b = u.first()
                s = u.suffix()
                for i in range(self.k): 
                    a = MonoidElem.from_char(i)
                    sa = s + a
                    self.log(3, f'a = {self.mc.to_string(a)}')
                    self.log(3, f'sa = {self.mc.to_string(sa)}')
                    # note, that each node represents irreducable string
                    # hence N.next is irreucable for each node N
                    # u is next of some node
                    # that means u is irreducable,
                    # so we only have to check sa
                    if self.table[s].pua_flag[i] == False: # sa is not reduced
                        self.log(4, f'sa is reducable')
                        r = self.table[s].pua[i]
                        print('r is ', r)
                        if r.is_identity():
                            self.table[u].pua.append(b)
                            self.table[u].pua_flag.append(False)
                            self.log(
                                4,
                                f'{self.mc.to_string(u)}.pua[{self.mc.to_string(a)}] ' +
                                f':= {self.mc.to_string(b)}')
                        else:
                            new_pua = self.table[self.table[r.prefix(
                            )].pau[b.letter()]].pua[r.last().letter()]
                            self.table[u].pua.append(new_pua)
                            self.table[u].pua_flag.append(False)
                            self.log(
                                4,
                                f'{self.mc.to_string(u)}.pua[{self.mc.to_string(a)}] '+ \
                                    f':= {self.mc.to_string(new_pua)}')
                   
                    else: # sa is irreducable
                        self.log(4, f'sa is irreducable')
                        ua_val = self.table[u].value * \
                            self.mc.generators[i]
                        # looking for u': u' < ua && val(u') == val(ua)
                        for u_short, node in self.table.items():
                            if ua_val == node.value and self.mc.compare(u_short, u+a) == -1:
                                self.log(
                                    4,
                                    f'adding rule: {self.mc.to_string(u+a)} -> ' +
                                    f'{self.mc.to_string(u_short)}')
                                self.rules.add_rule(u+a, u_short)
                                self.table[u].pua.append(u_short)
                                self.table[u].pua_flag.append(False)
                                self.table[u+a] = node
                                break
                        # we haven't faced ua_val before - create new node
                        else:
                            # we always have at least one next word
                            self.table[last].next = u+a
                            new_node = ExtendedNode(
                                value=ua_val,
                                first=u.first(),
                                last=a,
                                prefix=u,
                                suffix=u.suffix()+a,
                                len=len(u)+1,
                                next=MonoidElem.identity()
                            )
                            self.table[u+a] = new_node
                            last = u+a
                            self.log(
                                4, f'new unique value: {self.mc.to_string(u+a)} = {ua_val}')

                            self.table[u].pua.append(u+a)
                            self.table[u].pua_flag.append(True)
                # break iterating words of curlen
                # if we didnt find next irreducable word of curlen
                if u == last:
                    break
                u = self.table[u].next

            self.log(1, f'well, all uais are computed:')
            self.log(1, f'now compute all aus')

            # set u as smallest word of curlen
            u = v
            # calculate au for each u of len cur_len
            while len(u) == cur_len:
                p = u.prefix()
                lu = u.last().letter()
                for i in range(self.k):
                    ap = self.table[p].pau[i]
                    pau = self.table[ap].pua[lu]
                    self.table[u].pau.append(pau)
                    self.log(
                        2,
                        f'{self.mc.to_string(u)}.pau[{self.mc.to_string(MonoidElem.from_char(i))}] := ' +
                        f'{self.mc.to_string(pau)}')
                u = self.table[u].next
            # set u as first word of curlen+1
            v = u
            cur_len += 1

            self.draw_table()
            self.log(1, f'\n\n')