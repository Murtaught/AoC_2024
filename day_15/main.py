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
                fld.append(list(line))
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
    assert c in ['@', '.', 'O']
    fld[pos.i][pos.j] = c


cur_pos = find(fld, '@')
for instr in instrs:
    next = cur_pos.step(instr)
    what = get(next)

    match what:
        case '#' | None: 
            # Solid wall
            pass

        case '.':
            set(cur_pos, '.')
            set(next, '@')
            cur_pos = next

        case 'O':
            box_pos = next
            while get(box_pos) == 'O':
                box_pos = box_pos.step(instr)
            
            match get(box_pos):
                case None:
                    raise RuntimeError('Unwalled field!')

                case '#':
                    # Solid wall
                    pass

                case '.':
                    set(box_pos, 'O')
                    set(cur_pos, '.')
                    set(next, '@')
                    cur_pos = next
                    continue

                case _:
                    raise RuntimeError(f"Unexpected sybol at moved box position: '{get(box_pos)}'")


ans_p1 = 0
for i in range(N):
    for j in range(M):
        if fld[i][j] == 'O':
            ans_p1 += i * 100 + j

print("ans (p1):", ans_p1)
