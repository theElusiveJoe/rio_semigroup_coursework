from monoid import MonoidElem
import sys
sys.path.append(f'{sys.path[0]}/..')


m1 = MonoidElem.from_seq([1, 2, 3])
print(m1, m1.symbols)

m2 = MonoidElem.from_seq([4, 5, 6])
print(m2, m2.symbols)


m3 = m1 + m2
print(m3, m3.symbols)

print(m3.first(), m3.last())
print(m3.prefix(), m3.suffix())
print(m3.is_identity())

print(
    MonoidElem.identity(),
    MonoidElem.identity().symbols,
    MonoidElem.identity().is_identity())
