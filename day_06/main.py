# Input
with open("input") as file:
    fld = [list(line.strip()) for line in file]

n = len(fld)
m = len(fld[0])

# Helper functions
def get(i, j):
    if 0 <= i and 0 <= j and i < n and j < m:
        return fld[i][j]
    return None

def move(i, j, dir):
    if dir == '^': return (i - 1, j)
    if dir == '>': return (i, j + 1)
    if dir == 'v': return (i + 1, j)
    if dir == '<': return (i, j - 1)
    return None

def turn_right(dir):
    if dir == '^': return '>'
    if dir == '>': return 'v'
    if dir == 'v': return '<'
    if dir == '<': return '^'
    return None

def find(c):
    for i in range(n):
        for j in range(m):
            if fld[i][j] == c:
                fld[i][j] = '.'
                return (i, j)
    return None

START_DIR = '^'
START_POS = find(START_DIR)

# Solution (Part 1)
def solve_p1(pos, dir):
    visited = set()

    while get(*pos) != None:
        visited.add(pos)

        next = move(*pos, dir)
        c = get(*next)

        if c == '#':
            dir = turn_right(dir)
            continue

        assert(c == '.' or c == None)
        pos = next

    return len(visited)

print("ans_p1:", solve_p1(START_POS, START_DIR))

# Solution (Part 2)
def loops(pos, dir):
    visited = set()

    while get(*pos) != None:
        key = (*pos, dir)
        if key in visited:
            return True

        visited.add(key)

        next = move(*pos, dir)
        c = get(*next)

        if c == '#':
            dir = turn_right(dir)
            continue

        assert(c == '.' or c == None)
        pos = next

    return False

def solve_p2():
    count = 0
    for i in range(n):
        # print(f"Processing row {i} / {n} ...")
        for j in range(m):
            if get(i, j) == '.' and (i, j) != START_POS:
                fld[i][j] = '#'
                if loops(START_POS, START_DIR):
                    count += 1
                fld[i][j] = '.'
    return count

print("ans (p2):", solve_p2())
