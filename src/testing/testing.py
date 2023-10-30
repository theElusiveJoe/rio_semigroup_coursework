from monoid.monoid_controller import MonoidController
from monoid.monoid_elem import MonoidElem
from random import randint

def check_trs_correctness(
        mc:MonoidController, 
        rules:list[tuple[MonoidElem, MonoidElem]]
    ):

    me = MonoidElem([randint(0, len(mc.generating)-1) for _ in range(100)])
    print(me)
    true_val = mc.evaluate(me)
    simple_me = me.simplify(rules)
    simple_val = mc.evaluate(simple_me)
    assert true_val == simple_val
    print('TRS is correct!!')

