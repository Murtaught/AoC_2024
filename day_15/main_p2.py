from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    i: int
    j: int

    def step(self, dir):
        match dir:
            case '^': return Pos(self.i - 1, self.j)
            case '>': return Pos(self.i, self.j + 1)
            case 'v': return Pos(self.i + 1, self.j)
            case '<': return Pos(self.i, self.j - 1)
        return None


def read_input(filename):
    seen_empty_line = False
    fld = []
    instrs = []

    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not seen_empty_line:
                if line == '':
                    seen_empty_line = True
                    continue

                row = []
                for c in list(line):
                    match c:
                        case '#':
                            row += list("##")
                        case 'O':
                            row += list("[]")
                        case '.':
                            row += list("..")
                        case '@':
                            row += list("@.")
                fld.append(row)

            else:
                instrs += list(line)

    n = len(fld)
    m = len(fld[0])

    return fld, instrs

def find(fld, c) -> Pos:
    for i in range(len(fld)):
        for j in range(len(fld[i])):
            if fld[i][j] == c:
                return Pos(i, j)
    return None

########
# Main #
########
fld, instrs = read_input("input")
N, M = len(fld), len(fld[0])

def show_field():
    print(f"n: {N}, m: {M}")
    for row in fld:
        print(''.join(row))
    print()

def get(pos):
    if pos.i < 0 or pos.j < 0 or pos.i >= N or pos.j >= M:
        return None
    return fld[pos.i][pos.j]

def set(pos, c):
    assert pos.i >= 0
    assert pos.j >= 0
    assert pos.i <  N
    assert pos.j <  M
    assert c in ['@', '.', '[', ']']
    fld[pos.i][pos.j] = c

def have_box_at(pos):
    c = get(pos)
    return c == '[' or c == ']'

def other_end(pos):
    match get(pos):
        case '[':
            return Pos(pos.i, pos.j + 1)
        case ']':
            return Pos(pos.i, pos.j - 1)
        case _:
            raise RuntimeError("Not a box")

# `box_pos` is always the top-left position of the box,
# i.e. of '[' character.
def can_move(pos, dir, cache):
    key = (pos, dir)
    if key not in cache:
        next = pos.step(dir)

        # What is there?
        match get(next):
            case '.':
                cache[key] = True

            case '#' | None:
                # Solid wall.
                cache[key] = False

            case '[' | ']':
                if dir == '^' or dir == 'v':
                    cache[key] = \
                        can_move(next, dir, cache) and \
                        can_move(other_end(next), dir, cache)
                else:
                    cache[key] = can_move(next, dir, cache)

            case _:
                raise RuntimeError(f"Unexpected sybol: '{get(next)}'")
    return cache[key]


def do_move(pos, dir):
    next = pos.step(dir)

    # What is there?
    match get(next):
        case '.':
            pass

        case '[' | ']':
            do_move(other_end(next), dir)
            do_move(next, dir)

        case _:
            raise RuntimeError(f"Unexpected sybol: '{get(next)}'")

    set(next, get(pos))
    set(pos, '.')


cur_pos = find(fld, '@')
for instr in instrs:
    if can_move(cur_pos, instr, {}):
        do_move(cur_pos, instr)
        cur_pos = cur_pos.step(instr)

ans_p2 = 0
for i in range(N):
    for j in range(M):
        if fld[i][j] == '[':
            ans_p2 += i * 100 + j

print("ans (p2):", ans_p2)
