from universes.transformations import Transformation
from generating_sets import GeneratingSetsFamily
import random


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
    [5, 5, 5, 3, 5],  # лишний переход
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


'''
две независимые полугруппы и переходики между ними
'''

sg1 = [
    [2,1,3,4,5,6],
    [2,3,1,4,5,6],
    [1,1,3,4,5,6],
]
sg2 = [
    [1,2,3,4,4,6],
    [1,2,3,5,6,4],
]
transit = [
    [4,5,6,1,2,3]
]

two_independend = build_gsf(
    Transformation,
    sg1,sg2,transit
)

'''
две независимые полугруппы и переходики между ними
'''

def random_list(a: int, b: int, l: int):
    '''
    возвращает список длинны l с рандомными числами от a до b включительно
    '''
    return [random.randint(a,b) for _ in range(l)]


def gen_2_semigs(l1: int, l2:int, s1: int, s2: int, s3: int):
    '''
    l1 - мощность множества, на которое действует первая полугруппа

    l2 - мощность множества, на которое действует вторая полугруппа

    s1 - количество порождающих первую полугруппу
    
    s2 - количество порождающих вторую полугруппу

    s3 - количество свапов между элементами групп
    '''
    const1 = [i+1 for i in range(l1)]
    const2 = [l1+i+1 for i in range(l2)]

    e1 = lambda: random_list(1, l1, l1)
    e2 = lambda: random_list(l1+1, l2+l1, l2)

    sg1 = [
        e1() + const2
        for _ in range(s1) 
    ]
    sg2 = [
        const1 + e2()
        for _ in range(s2) 
    ]

    e3 = lambda: random.choice([e1,e2])() + random.choice([e1,e2])() 
    trans = [
        e3()
        for _ in range(s3)
    ]
    print('sg1:', sg1)
    print('sg2:', sg2)
    print('sg3:', trans)
    return build_gsf(
    Transformation,
    sg1,sg2,trans
    )


'''
две произвольные полугруппы
'''


def gen_2_random(t: int, s1: int, s2:int):
    return build_gsf(
        Transformation,
        [random_list(1, t, t) for _ in range(s1)],
        [random_list(1, t, t) for _ in range(s2)],
    )
