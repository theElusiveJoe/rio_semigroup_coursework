from generating_sets import GeneratingSet, GeneratingSetsFamily
from functools import reduce
from itertools import starmap
from pprint import pp

from .military_algo import MilitaryAlgo
from .crossing_algo import CrossingAlgo
from .semigroup_repr import SemigroupRepr


def buld_srki(gsf: GeneratingSetsFamily):
    generating_sets = gsf.get_all_generating_sets()
    srki = [MilitaryAlgo(*gs.to_mc_and_sigma()).run()
            for gs in generating_sets]
    return srki


def cmp_to_military(res: SemigroupRepr, gsf: GeneratingSetsFamily):
    mil_res = AlgosComposer.militaristic(gsf)

    srs_cross = res.get_srs()
    srs_mil = mil_res.get_srs()

    if srs_cross == srs_mil:
        return

    print('cross srs:')
    pp([f'    {k} -> {srs_cross[k]}' for k in sorted(srs_cross)])

    print('mil srs:')
    pp([f'    {k} -> {srs_mil[k]}' for k in sorted(srs_mil)])

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
        for k in common_keys
        if srs_cross[k] != srs_mil[k]})

    raise RuntimeError('results didn`t match!!!')


class AlgosComposer:

    @staticmethod
    def militaristic(gsf: GeneratingSetsFamily):
        return MilitaryAlgo(*gsf.to_one_generating_set().to_mc_and_sigma()).run()

    @staticmethod
    def crossing_chain_like(gsf: GeneratingSetsFamily, assert_check=True):
        srki = buld_srki(gsf)
        res = reduce(lambda x, y: CrossingAlgo(x, y).run(), srki)

        if assert_check:
            cmp_to_military(res, gsf)

        return res

    @staticmethod
    def crossing_tree_like(gsf: GeneratingSetsFamily, assert_check=True):
        def crossing_wrap(sr1: SemigroupRepr, sr2: SemigroupRepr | None):
            if sr2 is None:
                return sr1
            return CrossingAlgo(sr1, sr2).run()

        def loop(srki: list[SemigroupRepr]):
            match len(srki):
                case 0:
                    raise RuntimeError('impossible!')
                case 1:
                    return srki[0]
                case _:
                    if len(srki) % 2 == 1:
                        srki += [None]  # type: ignore
                    return loop(list(starmap(crossing_wrap, zip(srki[::2], srki[1::2]))))

        res = loop(buld_srki(gsf))

        if assert_check:
            cmp_to_military(res, gsf)

        return res
