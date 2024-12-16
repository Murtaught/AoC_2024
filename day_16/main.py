from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


# "Infinite" integer.
# At least for our purposes.
INF = 1_000_000_000

class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def turn_right(self) -> Dir:
        return Dir((self.value + 1) % 4)

    def turn_left(self) -> Dir:
        return Dir((self.value - 1) % 4)


@dataclass(frozen=True)
class Pos:
    i: int
    j: int

    def step(self, dir: Dir, steps: int = 1) -> Pos:
        match dir:
            case Dir.N: return Pos(self.i - steps, self.j)
            case Dir.E: return Pos(self.i, self.j + steps)
            case Dir.S: return Pos(self.i + steps, self.j)
            case Dir.W: return Pos(self.i, self.j - steps)
        raise RuntimeError(f"Unexpected Dir value: {dir}.")


@dataclass(frozen=True)
class State:
    pos: Pos
    dir: Dir

    def step(self, steps: int = 1) -> State:
        return State(
            self.pos.step(self.dir, steps), 
            self.dir
        )

    def turn_right(self) -> State:
        return State(self.pos, self.dir.turn_right())

    def turn_left(self) -> State:
        return State(self.pos, self.dir.turn_left())


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
        match self.get(pos.i, pos.j):
            case '.' | 'S' | 'E':
                return True
            case _:
                return False

    def find(self, c: str) -> Optional[Pos]:
        for i in range(self.height()):
            for j in range(self.width()):
                if self.fld[i][j] == c:
                    return Pos(i, j)
        return None

    def dijkstra(self, start: State, target: Pos) -> Tuple[dict[State, int], dict[State, list[State]]]:
        dist: dict[State, int] = {}
        dist[start] = 0

        came_from: dict[State, list[State]] = {}
        came_from[start] = []

        done: set[State] = set()

        while True:
            # Select the closest state fron the queue.
            cur = None
            cur_dist = INF

            for v, d in dist.items():
                if (v not in done) and (d < cur_dist):
                    cur = v
                    cur_dist = d

            if cur == None:
                # Exhausted the entire graph.
                break

            assert cur

            # Let's try to relax paths to neighbors.
            for next, dcost in [(cur.step(), 1), (cur.turn_right(), 1000), (cur.turn_left(), 1000)]:
                cost = cur_dist + dcost
                next_cost = dist.get(next, INF)
                if self.is_passable(next.pos):
                    if cost < next_cost:
                        dist[next] = cost
                        came_from[next] = [cur]

                    elif cost == next_cost:
                        came_from[next].append(cur)

            done.add(cur)

        return dist, came_from


fld = Field.read_file("input")
# fld.show()

start = fld.find('S')
assert start

target = fld.find('E')
assert target

dist, came_from = fld.dijkstra(State(start, Dir.E), target)

ans_p1 = INF
target_state: State
for dir in [Dir.N, Dir.E, Dir.S, Dir.W]:
    s = State(target, dir)
    d = dist.get(s, INF)
    if d < ans_p1:
        ans_p1 = d
        target_state = s

assert target_state
print("ans (p1):", ans_p1)

visited: set[Pos] = set()
queue = [target_state]
while queue:
    cur = queue.pop(0)
    visited.add(cur.pos)
    queue += came_from[cur]

print("ans (p2):", len(visited))
