# Input
deps = {}
lists = []

with open("input") as file:
    reading_rules = True
    for line in file:
        line = line.strip()
        if reading_rules:
            if not line:
                reading_rules = False
                continue

            # Rules ("X|Y"):
            x, y = map(int, line.split('|'))

            if y not in deps:
                deps[y] = []
            deps[y].append(x)

        else:
            # Lists
            xs = list(map(int, line.split(',')))
            lists.append(xs)

# Solution
def is_in_correct_order(xs):
    visited = set()
    for x in xs:
        # All dependencies of `x` must already be visited.
        for d in deps.get(x, []):
            if (d not in visited) and (d in xs):
                return False
        visited.add(x)
    return True

def mid_element(xs):
    n = len(xs)
    assert n % 2 == 1
    return xs[n // 2]

def fix_incorrect_order(xs):
    visited = set()
    fixed = []

    def visit(x):
        if x in visited:
            return

        for d in deps.get(x, []):
            if d in xs:
                visit(d)

        assert x not in visited
        fixed.append(x)
        visited.add(x)

    for x in xs:
        visit(x)

    return fixed

ans_p1 = 0
ans_p2 = 0
for xs in lists:
    if is_in_correct_order(xs):
        ans_p1 += mid_element(xs)
    else:
        ans_p2 += mid_element(fix_incorrect_order(xs))

print("ans (p1):", ans_p1)
print("ans (p2):", ans_p2)
