import sys
sys.path.append(f'{sys.path[0]}/..')

from pprint import pp
from functools import reduce
from algos.factorized import MilitaryAlgo, CrossingAlgo
from generating_sets import GeneratingSet, GeneratingSetsFamily
import samples


def run_military_from_gsf(gsf: GeneratingSetsFamily):
    return MilitaryAlgo(*gsf.to_one_generating_set().to_mc_and_sigma()).run()


def run_crossing_from_gsf(gsf: GeneratingSetsFamily):
    generating_sets = gsf.get_all_generating_sets()
    srki = [MilitaryAlgo(*gs.to_mc_and_sigma()).run()
            for gs in generating_sets]
    base_sr = reduce(lambda x, y: CrossingAlgo(x, y).run(), srki)
    return base_sr


def run_crossing_sample(gsf: GeneratingSetsFamily):
    military_sr = run_military_from_gsf(gsf)
    base_sr = run_crossing_from_gsf(gsf)

    srs_cross = base_sr.get_srs()
    srs_mil = military_sr.get_srs()

    print('cross srs:')
    pp(srs_cross)

    print('mil srs:')
    pp(srs_mil)

    keys1 = set(srs_cross.keys())
    keys2 = set(srs_mil.keys())

    only_keys1 = keys1.difference(keys2)
    only_keys2 = keys2.difference(keys1)
    common_keys = keys1.intersection(keys2)

    print('only crossing keys:')
    pp({k: srs_cross[k] for k in only_keys1})

    print('only military keys:')
    pp({k: srs_mil[k] for k in only_keys2})

    print('common keys with different values')
    pp({k: (srs_cross[k], srs_mil[k])
       for k in common_keys if srs_cross[k] != srs_mil[k]})

    assert military_sr == base_sr
    # print('IT WORKED!')


# run_crossing_sample(samples.crossing_samples.t5_rozen)
run_crossing_sample(samples.crossing_samples.t5_rozen_broken)
