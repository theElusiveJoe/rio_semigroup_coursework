from universes.transformations import Transformation
from generating_sets import GeneratingSet

build_gs = GeneratingSet.build_from_description

'''
пример из статьи
'''

t6_paper_example = build_gs(
    Transformation,
    [2, 2, 4, 4, 5, 6],
    [5, 3, 4, 4, 6, 6],
)

'''
порождающие всю полугруппу трансформаций
'''

t4_entire = build_gs(
    Transformation,
    [1, 1, 3, 4],  # merge
    [2, 3, 4, 1],  # cycle
    [2, 1, 3, 4],  # swap
)

t3_entire = build_gs(
    Transformation,
    [1, 1, 3],  # merge
    [2, 3, 1],  # cycle
    [2, 1, 3],  # swap
)


'''
порождающие всю группу перестановок
'''

t6_permutations = build_gs(
    Transformation,
    [2, 3, 4, 5, 6, 1],  # cycle
    [2, 1, 3, 4, 5, 6],  # swap
)


'''
ничего нового не порождается
'''

t6_two_elems = build_gs(
    Transformation,
    [1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2],
)

'''
главные идеалы
'''

t6_principal_ideal = build_gs(
    Transformation,
    [2, 3, 4, 5, 6, 1],
)
