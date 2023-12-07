from .order_config import OrderConfig


MILITARY_ORDER = OrderConfig(
    add_func=lambda frontier, new_elems: frontier.extend(new_elems),
    pop_func=lambda frontier: frontier.pop(0),
    desc='military order',
)


LEX_ORDER = OrderConfig(
    add_func=lambda frontier, new_elems: frontier.extend(new_elems[::-1]),
    pop_func=lambda frontier: frontier.pop(-1),
    desc='lg order',

)
