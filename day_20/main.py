from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Callable, Generator


class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


@dataclass(frozen=True)
class Pos:
    i: int
    j: int

    def ord(self) -> int:
        return (self.i << 16) + self.j

    def step(self, dir: Dir, steps: int = 1) -> Pos:
        match dir:
            case Dir.N: return Pos(self.i - steps, self.j)
            case Dir.E: return Pos(self.i, self.j + steps)
            case Dir.S: return Pos(self.i + steps, self.j)
            case Dir.W: return Pos(self.i, self.j - steps)
        raise RuntimeError(f"Unexpected Dir value: {dir}.")

CharMatrix = list[list[str]]

class Field:
    fld: CharMatrix

    def __init__(self, fld: CharMatrix):
        self.fld = fld

    @staticmethod
    def read_file(filename: str) -> Field:
        with open(filename) as file:
            return Field([list(line.strip()) for line in file])
    
    def height(self) -> int:
        return len(self.fld)

    def width(self) -> int:
        return len(self.fld[0])

    def show(self) -> None:
        for i in range(self.height()):
            for j in range(self.width()):
                print(self.fld[i][j], end='')
            print()
        print()

    def get(self, i: int, j: int) -> Optional[str]:
        if i < 0 or j < 0 or i >= self.height() or j >= self.width():
            return None
        return self.fld[i][j]

    def is_passable(self, pos: Pos) -> bool:
        return self.get(pos.i, pos.j) in ['.', 'S', 'E']

    def find(self, c: str) -> Optional[Pos]:
        for i in range(self.height()):
            for j in range(self.width()):
                if self.fld[i][j] == c:
                    return Pos(i, j)
        return None

    def bfs(self, start: Pos) -> dict[Pos, int]:
        dist: dict[Pos, int] = {}
        dist[start] = 0

        queue = deque([start])
        while queue:
            cur = queue.popleft()
            cur_dist = dist[cur]

            for dir in [Dir.N, Dir.E, Dir.S, Dir.W]:
                next = cur.step(dir)
                if self.is_passable(next) and next not in dist:
                    dist[next] = cur_dist + 1
                    queue.append(next)

        return dist

    def all(self) -> Generator[Pos, None, None]:
        for i in range(self.height()):
            for j in range(self.width()):
                yield Pos(i, j)


FLD = Field.read_file("input")
# FLD.show()

START = FLD.find('S')
assert START

END = FLD.find('E')
assert END

DISTS = FLD.bfs(END)
# print("shortest dist w/o cheating:", DISTS[START])

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a.i - b.i) + abs(a.j - b.j)

# Solution
ans_p1 = 0
ans_p2 = 0

# speedups: defaultdict[int, set[Tuple[Pos, Pos]]] = defaultdict(lambda: set())

for a in FLD.all():
    if not FLD.is_passable(a):
        continue

    for b in FLD.all():
        if not FLD.is_passable(b):
            continue

        m = manhattan(a, b)
        if 0 < m <= 20:
            da = DISTS[a]
            db = DISTS[b]
            
            speedup = da - (db + m)
            if speedup >= 100:
                ans_p2 += 1

                if m <= 2:
                    ans_p1 += 1


# for speedup in sorted(speedups.keys()):
#     print(f'{speedup} => {len(speedups[speedup])}')
#     for a, b in speedups[speedup]:
#         print(f"    {a}  -- {manhattan(a, b)} -- {b} ({DISTS[b]}) ")

print("ans (p1):", ans_p1)
print("ans (p2):", ans_p2)
