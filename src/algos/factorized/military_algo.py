from monoid import MonoidController, MonoidElem, RulesSystem
from universes import Universe
from .node import Node


class MilitaryAlgo:
    mc: MonoidController
    sigma: list[int]
    rules: RulesSystem
    table: dict[MonoidElem, Node] = dict()
    value_table: dict[Universe, Node] = dict()

    def __init__(self, mc: MonoidController, sigma: list[int]) -> None:
        self.mc = mc
        self.sigma = sigma
        self.rules = RulesSystem(mc=self.mc)
        self.table = dict()
        self.value_table = dict()

    def draw_table(self):
        print('Table:')
        for k, v in self.table.items():
            print(f'    {self.mc.to_string(k)} -> ' +
                  f'{self.mc.to_string(v.retrieve_string())}: {v.value}')

    def run(self):
        self.setup()
        self.main_cycle()
        return self.rules

    def setup(self):
        id_node = Node(
            value=self.mc.identity(),
            first=MonoidElem.identity(),
            last=MonoidElem.identity(),
            prefix=MonoidElem.identity(),
            suffix=MonoidElem.identity(),
            len=0,
            next=MonoidElem.from_char(self.sigma[0]),
        )
        self.table[MonoidElem.identity()] = id_node
        self.value_table[self.mc.identity()] = id_node

        for i in self.sigma:
            a = MonoidElem.from_char(i)
            a_val = self.mc.generators[i]
            new_node = Node(
                value=a_val,
                first=a,
                last=a,
                prefix=MonoidElem.identity(),
                suffix=MonoidElem.identity(),
                len=1,
                next=MonoidElem.from_char(i+1)
                if i != self.sigma[-1] else MonoidElem.identity()
            )
            self.table[a] = new_node
            self.value_table[a_val] = new_node  

            id_node.pau[i] = MonoidElem.from_char(i)
            id_node.pua[i] = MonoidElem.from_char(i)
            id_node.pua_flag[i] = True

    def main_cycle(self):
        cur_len = 1
        u = MonoidElem([self.sigma[0]])
        v = u
        last = MonoidElem([self.sigma[-1]])

        while u != MonoidElem.identity():
            while len(u) == cur_len:
                b = u.first()
                s = u.suffix()
                for i in self.sigma:
                    a = MonoidElem.from_char(i)

                    # sa can be reduced
                    if self.table[s].pua_flag[i] == False:
                        # r is reduced sa  
                        r = self.table[s].pua[i]  
                        if r.is_identity():
                            new_pua = b
                        else:
                            t, c = r.prefix(), r.last().letter()
                            if t == s:
                                new_pua = self.table[u].pua[c]
                            else:
                                new_pua = self.table[self.table[t].pau[b.letter(
                                )]].pua[c]

                        self.table[u].pua[i] = new_pua
                        self.table[u].pua_flag[i] = False

                    # sa is irreducable
                    else: 
                        # compute val(ua) 
                        ua_val = self.table[u].value * self.mc.generators[i]
                        # looking for u': u' < ua && val(u') == val(ua)
                        u_short = self.value_table.get(ua_val)
                        # we already faced this value
                        if u_short is not None:
                            u_short_str = u_short.retrieve_string()
                            self.rules.add_rule(u+a, u_short_str)
                            self.table[u].pua[i] = u_short_str
                            self.table[u].pua_flag[i] = False
                            self.table[u+a] = u_short
                        # we haven't faced ua_val before - create new node
                        else:
                            ua = u + a
                            new_node = Node(
                                value=ua_val,
                                first=u.first(),
                                last=a,
                                prefix=u,
                                suffix=u.suffix()+a,
                                len=len(u)+1,
                                next=MonoidElem.identity()
                            )
                            self.table[ua] = new_node

                            self.table[last].next = ua
                            last = ua
                            
                            self.value_table[ua_val] = new_node
                            self.table[u].pua[i] = ua
                            self.table[u].pua_flag[i] = True

                if u == last:
                    break
                u = self.table[u].next

            # set u as smallest word of curlen
            u = v
            # calculate au for each u of len cur_len
            while len(u) == cur_len:
                p = u.prefix()
                lu = u.last().letter()
                for i in self.sigma:
                    ap = self.table[p].pau[i]
                    pau = self.table[ap].pua[lu]
                    self.table[u].pau[i] = pau
                u = self.table[u].next
            # set u as first word of curlen+1
            v = u
            cur_len += 1
