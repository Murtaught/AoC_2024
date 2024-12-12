# Input
with open("input") as file:
    fld = [list(line.strip()) for line in file]

n = len(fld)
m = len(fld[0])

# Preparation (finding and labeling all connectivity components)
comp_count = 0
comp = [[None for _ in range(m)] for _ in range(n)]

def get(mtx, i, j):
    if i < 0 or j < 0 or i >= n or j >= m:
        return None
    return mtx[i][j]

def fill(i, j, c, k):
    if get(fld, i, j) != c:
        return

    if get(comp, i, j) == k:
        return

    comp[i][j] = k

    fill(i - 1, j, c, k)
    fill(i, j + 1, c, k)
    fill(i + 1, j, c, k)
    fill(i, j - 1, c, k)

for i in range(n):
    for j in range(m):
        if comp[i][j] == None:
            fill(i, j, fld[i][j], comp_count)
            comp_count += 1

# Solution
# Finding areas
comp_area = [0] * comp_count
for i in range(n):
    for j in range(m):
        comp_area[comp[i][j]] += 1

# Finding perimeters
comp_perimeter = [0] * comp_count
for i in range(n):
    for j in range(m):
        c = fld[i][j]
        comp_perimeter[comp[i][j]] += \
            int(get(fld, i - 1, j) != c) + \
            int(get(fld, i, j + 1) != c) + \
            int(get(fld, i + 1, j) != c) + \
            int(get(fld, i, j - 1) != c)


# Finding count of sides
comp_sides = [0] * comp_count

for k in range(comp_count):
    for i in range(n):
        in_t = in_b = False
        for j in range(m):
            if comp[i][j] == k and comp[i][j] != get(comp, i - 1, j):
                if not in_t:
                    comp_sides[k] += 1
                    in_t = True
            else:
                in_t = False

    # Bottom
    for i in range(n):
        inside = False
        for j in range(m):
            if comp[i][j] == k and comp[i][j] != get(comp, i + 1, j):
                if not inside:
                    comp_sides[k] += 1
                    inside = True
            else:
                inside = False

    # Left
    for j in range(m):
        inside = False
        for i in range(n):
            if comp[i][j] == k and comp[i][j] != get(comp, i, j - 1):
                if not inside:
                    comp_sides[k] += 1
                    inside = True
            else:
                inside = False

    # Right
    for j in range(m):
        inside = False
        for i in range(n):
            if comp[i][j] == k and comp[i][j] != get(comp, i, j + 1):
                if not inside:
                    comp_sides[k] += 1
                    inside = True
            else:
                inside = False

print("ans (p1):", sum(comp_area[i] * comp_perimeter[i] for i in range(comp_count)))
print("ans (p2):", sum(comp_area[i] * comp_sides[i]     for i in range(comp_count)))
