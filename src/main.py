from universes.T_universe import T
from algos.simple_algo import SimpleAlgo
from monoid.monoid_controller import MonoidController
from testing.testing import check_trs_correctness

a = T([2,2,4,4,5,6])
b = T([5,3,4,4,6,6])

# a = T([2,3,4,5,6,1])
# b = T([1,1,3,4,5,6])

mc = MonoidController([a, b], ['a', 'b'])
algo = SimpleAlgo(mc)
rules = algo.run()
for l,r in rules:
    print(l, '->', r)


check_trs_correctness(mc, rules)



