from samples import crossing_samples as cs
from algos.factorized import AlgosComposer
from utils.timer import timer
from algos.factorized.dict_wrapper import AT
from pprint import pp

from utils.logger import set_log_lvl, LogFlags
set_log_lvl(LogFlags.NO)

import random
# random.seed(42)


def cmp(x):
    AT.reset()
    _, tm = timer(AlgosComposer.militaristic)(x)
    atm = AT.copy()
    pp(atm)
    
    AT.reset()
    _, tc = timer(AlgosComposer.crossing_tree_like)(x, assert_check=False)
    atc = AT.copy()
    pp(atc)

    sec_diff = tc - tm
    times_diff = tc/tm

    succ, times_diff = ('SLOWER', times_diff) if tc > tm else ('FASTER', 1/times_diff)
    print(f'\n>>🦤 diff {sec_diff}s')
    print(f'\n>>🦤 {succ} {times_diff:.2} times')

    
    return sec_diff < 0

total = 0
succ = 0
for i in range(1000):
    print('------------')
    # x = cs.gen_2_semigs(
    #     l1=4,
    #     l2=4,
    #     s1=2,
    #     s2=2,
    #     s3=3
    # )
    
    # x = cs.gen_2_semigs_simple_trans(
    #     l1=4,
    #     l2=4,
    #     s1=15,
    #     s2=15
    # )
    # x = cs.bebebe(6,4)
    # x = cs.two_ideals(6,6)

    x = cs.gen_n_random(3,[6,6])
    print(x)

    succ += cmp(x)
    total += 1

print(succ/total)
