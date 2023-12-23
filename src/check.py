from samples import crossing_samples as cs
from algos.factorized import AlgosComposer
from utils.timer import timer
from algos.factorized.dict_wrapper import AT
from pprint import pp

from utils.logger import set_log_lvl, LogFlags
set_log_lvl(LogFlags.BRIEF)

import random


def cmp(x):
    AT.reset()
    res, tm = timer(AlgosComposer.militaristic)(x)
    atm = AT.copy()
    pp(atm)
    
    AT.reset()
    res, tc = timer(AlgosComposer.crossing_tree_like)(x, assert_check=False)
    atc = AT.copy()
    pp(atc)

    sec_diff = tc - tm
    times_diff = tc/tm

    print(f'\n>>🦤 diff {sec_diff}s, slower in {times_diff:.2} times')

    if sec_diff < 0:
        raise RuntimeError('CROSSING IS FASTER LOL')

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
    
    x = cs.gen_n_random(7,[6,6])
    cmp(x)
    

