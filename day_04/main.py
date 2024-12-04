# Input
with open("input") as file:
    w = [list(line.strip()) for line in file]

n = len(w)

# (Input seems to be always a square)
for row in w:
    assert len(row) == n

# Solution (Part 1)
def get(i, j):
    if i >= 0 and j >= 0 and i < n and j < n:
        return w[i][j]
    return None

DIRS = [
    (-1,  0), # N
    (-1,  1), # NE
    ( 0,  1), # E
    ( 1,  1), # SE
    ( 1,  0), # S
    ( 1, -1), # SW
    ( 0, -1), # W
    (-1, -1), # NW
]

def check(i, j, dir):
    di, dj = dir
    for c in list("XMAS"):
        if get(i, j) != c:
            return False
        i += di
        j += dj
    return True

ans_p1 = 0
for i in range(n):
    for j in range(n):
        for dir in DIRS:
            if check(i, j, dir):
                ans_p1 += 1

print("ans (p1):", ans_p1)

# Solution (Part 2)
def check_mas(a, b):
    return (a == 'M' and b == 'S') or (a == 'S' and b == 'M')

ans_p2 = 0
for i in range(n):
    for j in range(n):
        if get(i, j) == 'A':
            if check_mas(get(i - 1, j - 1), get(i + 1, j + 1)):
                if check_mas(get(i - 1, j + 1), get(i + 1, j - 1)):
                    ans_p2 += 1

print("ans (p2):", ans_p2)
