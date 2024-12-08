from fractions import Fraction

# Input
with open("input") as file:
    fld = [list(line.strip()) for line in file]

n = len(fld)
m = len(fld[0])

ants = {}
for i in range(n):
    for j in range(m):
        c = fld[i][j]
        if c != '.':
            if c not in ants:
                ants[c] = []
            ants[c].append((i, j))


# Solution
def euclid_sq(a, b):
    ai, aj = a
    bi, bj = b
    return (ai - bi) ** 2 + (aj - bj) ** 2

def are_on_the_same_line(ps):
    ps.sort(key=lambda p: p[0] * m + p[1])
    assert len(ps) >= 3

    base_i, base_j = ps[0]
    first_i, first_j = ps[1]
    
    if base_i == first_i:
        # All must lie on row `base_i`.
        return all(map(lambda p: p[0] == base_i, ps))

    base = Fraction(first_j - base_j, first_i - base_i)
    for k in range(2, len(ps)):
        i, j = ps[k]
        frac = Fraction(j - base_j, i - base_i)
        if frac != base:
            return False

    return True

antinodes_p1 = set()
antinodes_p2 = set()

def check(p):
    global antinodes_p1
    global antinodes_p2
    for locs in ants.values():
        for i in range(len(locs)):
            antinodes_p2.add(locs[i])
            for j in range(i):
                if are_on_the_same_line([p, locs[i], locs[j]]):
                    antinodes_p2.add(p)
                    dist_a = euclid_sq(locs[i], p)
                    dist_b = euclid_sq(locs[j], p)
                    if dist_a == 4 * dist_b or dist_a * 4 == dist_b:
                        antinodes_p1.add(p)

for i in range(n):
    for j in range(m):
        check((i, j))

print("ans (p1):", len(antinodes_p1))
print("ans (p2):", len(antinodes_p2))

