from universes.transformations import Transformation
from testing.test_class import Test

t6_paper_example = Test(
    Transformation,
    [2, 2, 4, 4, 5, 6],
    [5, 3, 4, 4, 6, 6],
)

t4_entire = Test(
    Transformation,
    [1, 1, 3, 4],  # merge
    [2, 3, 4, 1],  # cycle
    [2, 1, 3, 4],  # swap
)

t3_entire = Test(
    Transformation,
    [1, 1, 3],  # merge
    [2, 3, 1],  # cycle
    [2, 1, 3],  # swap
)

t6_permutations = Test(
    Transformation,
    [2, 3, 4, 5, 6, 1],  # cycle
    [2, 1, 3, 4, 5, 6],  # swap
)

t6_two_elems = Test(
    Transformation,
    [1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2],
)

t6_identity = Test(
    Transformation,
    [1, 2, 3, 4, 5, 6],
)

t6_principal_ideal = Test(
    Transformation,
    [2, 3, 4, 5, 6, 1],
)

t5_f1 = Test(
    Transformation,
    [2, 5, 5, 5, 5],
    [5, 3, 5, 5, 5],
    [5, 5, 4, 5, 5],
    [5, 5, 5, 4, 5],
    [5, 5, 5, 5, 5],
)

t5_f2 = Test(
    Transformation,
    [5, 5, 5, 3, 5],
    [5, 5, 2, 5, 5],
    [5, 1, 5, 5, 5],
    [1, 5, 5, 5, 5],
    [5, 5, 5, 5, 5],
)

t4_f1 = Test(
    Transformation,
    [2, 3, 4, 1]
)

t4_f2 = Test(
    Transformation,
    [4, 1, 2, 3]
)
