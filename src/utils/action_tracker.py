from dataclasses import dataclass, field
from copy import copy


@dataclass
class ActionTracker:
    expect_to_check: int = field(default=0)
    checked_real: int = field(default=0)
    skipped_as_bs: int = field(default=0)
    reduced_by_str: int = field(default=0)
    reduced_by_value: int = field(default=0)
    replaced_old_strings: int = field(default=0)
    new_values_found: int = field(default=0)
    table_lookups: int = field(default=0)
    monoids_created: int = field(default=0)

    def reset(self):
        [setattr(self, attr, 0)
         for attr in dir(self)
         if not attr.startswith('_') and isinstance(getattr(self, attr), int)]

    def copy(self):
        return copy(self)


AT = ActionTracker()
