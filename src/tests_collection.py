from typing import NamedTuple, Any, Callable, Iterable, Literal

import samples.crossing_samples as cs
from utils.testing_system import TestingSample, run_many


test_workpieces = ([
    # разные розены
    # (cs.rozen, [(5,), (7,)], 1),
    # (cs.rozen2, [(5,), (7,)], 1),

    # автомат - кольцо
    # (cs.two_cycles, [(10,), (15,)], 5),

    # автомат зигера - типа полносвязный
    # (cs.ziggy, [(6,)], 5),

    # две полугруппы
    # (cs.two_semigs, [(5, 1, 2), (3, 5, 5), (4, 2, 1)], 1),
    # (cs.two_semigs_st, [(5, 1), (6, 1),], 1),

    # произвольные полугрупп
    (cs.random_sg, [(5, 4, 6), (7, 1, 2)], 5),

    # какие-то мои придумки ¯\_(ツ)_/
    # (cs.dopplers, [(5, 3), (6, 2)], 3),
    # (cs.two_ideals, [(5, 5), (8, 3)], 3),
    # (cs.independenties,  [(5, 5), (8, 3)], 3),
    # (cs.ind_dopplers,  [(5, 5), (8, 3)], 3),
    # (cs.prism,  [(5, 3, 3), (6, 2, 3)], 3),
])


TESTS_COLLECTION = list(map(
    lambda x: TestingSample(*x),  # type: ignore
    test_workpieces
))
