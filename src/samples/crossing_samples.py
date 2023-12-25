from universes.transformations import Transformation
from generating_sets import GeneratingSetsFamily
import random


build_gsf = GeneratingSetsFamily.build_from_description


'''
автомат с самой плохой декомпозицией
'''


def rozen(n: int):
    t1 = [
        [i + 2 if i == j else n for i in range(n)]
        for j in range(n - 2)
    ]
    t1.append([n - 1 if i == n - 2 else n for i in range(n)])
    t1.append([n for _ in range(n)])

    t2 = [
        [i if i - 1 == j else n for i in range(n)]
        for j in range(n - 2)
    ]
    t2.insert(0, [1 if i == 0 else n for i in range(n)])
    t2.append([n for _ in range(n)])

    return build_gsf(
        Transformation,
        t1, t2
    )


def rozen2(n: int):
    t1 = [
        [i + 2 if i == j else n for i in range(n)]
        for j in range(n - 2)
    ]
    t1.append([n - 1 if i == n - 2 else n for i in range(n)])
    t1.append([n for _ in range(n)])

    t2 = [
        [i if i - 1 == j else n for i in range(n)]
        for j in range(n - 2)
    ]
    t2.insert(0, [1 if i == 0 else n for i in range(n)])
    t2.append([n for _ in range(n)])

    t3, t4 = t1[:len(t1) // 2] + t2[:len(t2) //
                                    2], t1[len(t1) // 2:] + t2[len(t2) // 2:]

    return build_gsf(
        Transformation,
        t3, t4
    )


def two_cycles(n: int):
    t1 = [
        [i + 2 if i == j else n for i in range(n - 1)] + [n]
        for j in range(n - 2)
    ] + [[1 if i == n - 2 else n for i in range(n - 1)] + [n]]

    t2 = [[n - 1 if i == 0 else n for i in range(n - 1)] + [n]] + [
        [i if i == j else n for i in range(n - 1)] + [n]
        for j in range(1, n - 1)
    ]
    return build_gsf(
        Transformation,
        t1, t2
    )


def ziggy(n: int):
    s = {i: random.sample(list(range(1, n + 1)), n) for i in range(1, n + 1)}
    print(s)
    t1 = [
        [s[i + 1].pop() for i in range(n)]
        for _ in range(n)
    ]

    return build_gsf(
        Transformation,
        t1[:len(t1) // 2], t1[len(t1) // 2:]
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
    [2, 1, 3, 4, 5, 6],
    [2, 3, 1, 4, 5, 6],
    [1, 1, 3, 4, 5, 6],
]
sg2 = [
    [1, 2, 3, 4, 4, 6],
    [1, 2, 3, 5, 6, 4],
]
transit = [
    [4, 5, 6, 1, 2, 3]
]

two_independend = build_gsf(
    Transformation,
    sg1, sg2, transit
)

'''
две независимые полугруппы и переходики между ними
'''


def random_list(a: int, b: int, l: int):
    '''
    возвращает список длинны l с рандомными числами от a до b включительно
    '''
    return [random.randint(a, b) for _ in range(l)]


def two_semigs(l1: int, s1: int, s3: int):
    '''
    l1 - мощность множества, на которое действует первая полугруппа

    s1 - количество порождающих первую полугруппу

    s3 - количество свапов между элементами групп
    '''
    const1 = [i + 1 for i in range(l1)]
    const2 = [l1 + i + 1 for i in range(l1)]

    def e1(): return random_list(1, l1, l1)
    def e2(): return random_list(l1 + 1, l1 + l1, l1)

    sg1 = [
        e1() + const2
        for _ in range(s1)
    ]
    sg2 = [
        const1 + e2()
        for _ in range(s1)
    ]

    def e3(): return random.choice([e1, e2])() + random.choice([e1, e2])()
    trans = [
        e3()
        for _ in range(s3)
    ]
    return build_gsf(
        Transformation,
        sg1, sg2, trans
    )


def two_semigs_st(l1: int, s1: int):
    '''
    l1 - мощность множества, на которое действует первая полугруппа

    l2 - мощность множества, на которое действует вторая полугруппа

    s1 - количество порождающих первую полугруппу

    s2 - количество порождающих вторую полугруппу
    '''
    const1 = [i + 1 for i in range(l1)]
    const2 = [l1 + i + 1 for i in range(l1)]

    def e1(): return random_list(1, l1, l1)
    def e2(): return random_list(l1 + 1, l1 + l1, l1)

    sg1 = [
        e1() + const2
        for _ in range(s1)
    ]
    sg2 = [
        const1 + e2()
        for _ in range(s1)
    ]

    trans = [
        [l1 + 1 + i for i in range(l1)] + [1 + i for i in range(l1)]
    ]
    return build_gsf(
        Transformation,
        sg1, sg2, trans
    )


'''
несколько произвольных полугрупп
'''


def random_sg(t: int, s: int, n: int):
    '''
    t - мощность множества, на которое действует полугруппа
    s - количество порождающих каждуя полугруппу
    n - количество полугрупп
    '''
    return build_gsf(
        Transformation,
        *[[random_list(1, t, t) for _ in range(s)] for _ in range(n)],
    )


'''
какие-то частные случаи
'''


def dopplers(n: int, k: int):
    '''
    n - модность множества
    k - количество порождающих
    '''
    const1 = [i + 1 for i in range(n)]
    const2 = [n + i + 1 for i in range(n)]

    def e1(): return random_list(1, n, n)
    t1 = [
        e1() for _ in range(k)
    ]
    t2 = [
        [y + n for y in x] for x in t1
    ]
    t1 = [x + const2 for x in t1]
    t2 = [const1 + x for x in t2]
    t3 = [
        list(range(n + 1, 2 * n + 1)) + list(range(1, n + 1))
    ]
    return build_gsf(
        Transformation,
        t1, t2
    )


def two_ideals(n: int, k: int):
    t1 = [
        random_list(1, n, n * 2)
        for _ in range(k)
    ]
    t2 = [
        random_list(n + 1, 2 * n, n * 2)
        for _ in range(k)
    ]

    return build_gsf(
        Transformation,
        t1, t2
    )


def independenties(n: int, s: int):
    const = [2 * n + 1] * n

    sg1 = [
        random_list(1, n, n) + const + [2 * n + 1]
        for _ in range(s)
    ]
    sg2 = [
        const + random_list(1 + n, n + n, n) + [2 * n + 1]
        for _ in range(s)
    ]
    return build_gsf(
        Transformation,
        sg1, sg2,
    )


def ind_dopplers(n: int, k: int):
    const = [n + 1 for i in range(n)]

    def e1(): return random_list(1, n, n)
    t1 = [
        e1() for _ in range(k)
    ]
    t2 = [
        [y + n for y in x] for x in t1
    ]
    t1 = [x + const + [2 * n + 1] for x in t1]
    t2 = [const + x + [2 * n + 1]for x in t2]

    return build_gsf(
        Transformation,
        t1, t2
    )


def prism(n: int, n1: int, s: int):
    const = [2 * n + 1 for _ in range(n)]
    # главная часть
    t1 = [
        const + random_list(n + 1, 2 * n, n) + [2 * n + 1]
        for _ in range(n)
    ]
    # переход
    t2 = [
        random_list(n + 1, 2 * n, n) +
        [2 * n + 1 for _ in range(n)] + [2 * n + 1]
        for _ in range(n1)
    ]
    # побочная часть
    t3 = [
        random_list(1, n, n) + const + [2 * n + 1]
        for _ in range(n)
    ]
    return build_gsf(
        Transformation,
        t1, t2, t3
    )
