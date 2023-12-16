from algos.random_order import Algo, OrderConfig, LEX_ORDER, MILITARY_ORDER
from monoid.controller import MonoidController
from samples import military_samples


def main():
    the_test = military_samples.t6_paper_example.generators
    mc = MonoidController(the_test)

    algo = Algo(
        mc=mc,
        order_cfg=MILITARY_ORDER,
    )
    res = algo.run()
    print(res)

    algo = Algo(
        mc=mc,
        order_cfg=LEX_ORDER,
    )
    res = algo.run()
    print(res)


if __name__ == '__main__':
    main()
