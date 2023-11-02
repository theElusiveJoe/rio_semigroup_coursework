from testing import tests


# algo = tests.t6_identity()  # should throw error
# algo = tests.t6_paper_example()
# algo = tests.t3_entire()
algo = tests.t4_entire()
# algo = tests.t6_principal_ideal()
# algo = tests.t6_permutations()
# algo = tests.t6_two_elems()

A = set([v.value for v in algo.table.values()])
print(f'total: {len(A)} elems')

# for x in A:
#     for y in A:
#         assert x*y in A