from universes.transformations import Transformation
from generating_sets import GeneratingSetsFamily

build_gsf = GeneratingSetsFamily.build_from_description


'''
автомат с самой плохой декомпозицией
'''

_t5_rozen_1 = [
    [2, 5, 5, 5, 5],
    [5, 3, 5, 5, 5],
    [5, 5, 4, 5, 5],
    [5, 5, 5, 4, 5],
    [5, 5, 5, 5, 5],
]
_t5_rozen_2 = [
    [5, 5, 5, 3, 5],
    [5, 5, 2, 5, 5],
    [5, 1, 5, 5, 5],
    [1, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
]

t5_rozen = build_gsf(
    Transformation,
    _t5_rozen_1,
    _t5_rozen_2,
)

'''
этот же автомат, но сломанный в одном месте
'''

_t5_rozen_broken_1 = [
    [2, 5, 5, 5, 5],
    [5, 3, 5, 5, 5],
    [5, 5, 4, 5, 5],
    [5, 5, 5, 4, 5],
    [5, 5, 5, 5, 5],
    [5, 5, 5, 3, 5], # лишний переход
]
_t5_rozen_broken_2 = [
    [5, 5, 5, 3, 5],
    [5, 5, 2, 5, 5],
    [5, 1, 5, 5, 5],
    [1, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
]

t5_rozen_broken = build_gsf(
    Transformation,
    _t5_rozen_broken_1,
    _t5_rozen_broken_2,
)
