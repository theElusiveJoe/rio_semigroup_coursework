from monoid.element import MonoidElem
from monoid.controller import MonoidController


class Rule():
    lhs: MonoidElem
    rhs: MonoidElem

    def __init__(self, l: MonoidElem, r: MonoidElem) -> None:
        self.lhs, self.rhs = l, r

    def __len__(self):
        return len(self.lhs)

    def apply(self, target: MonoidElem):
        for i in range(len(target)):
            if target.symbols[i:i+len(self)] == self.lhs.symbols:
                return MonoidElem(
                    target.symbols[:i] +
                    self.rhs.symbols +
                    target.symbols[i+len(self):]
                ), True
        return target, False

    def __repr__(self):
        return f'{self.lhs} -> {self.rhs}'


class RulesSystem:
    rules: list[Rule]
    mc: MonoidController | None

    def __init__(self, mc: MonoidController | None = None) -> None:
        self.rules = []
        self.mc = mc

    def __repr__(self):
        if self.mc is None:
            return '#'*30 + '\n' + '\n'.join(map(repr, self.rules)) + '\n' + '#'*30 + '\n'

        s = '#'*30 + '\n'
        for rule in self.rules:
            s += f'    {self.mc.to_string(rule.lhs)} -> {self.mc.to_string(rule.rhs)}\n'
        s += '#'*30 + '\n'
        return s

    def add_rule(self, lhs: MonoidElem, rhs: MonoidElem):
        self.rules.append(Rule(lhs, rhs))

    def apply(self, target: MonoidElem):
        changed_flag = True
        while changed_flag:
            changed_flag = False
            for rule in self.rules:
                target, flag = rule.apply(target)
                changed_flag |= flag
        return target
