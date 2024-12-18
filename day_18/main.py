from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import re

N: int
P1_PREFIX: int
WALLS: list[Pos]

@dataclass(frozen=True)
class Pos:
    i: int
    j: int

    @staticmethod
    def parse(s: str) -> Pos:
        i, j = map(int, s.split(','))
        return Pos(i, j)

    def step(self, dir: str) -> Pos:
        match dir:
            case '^': 
                return Pos(self.i - 1, self.j)
            case '>': 
                return Pos(self.i, self.j + 1)
            case 'v': 
                return Pos(self.i + 1, self.j)
            case '<': 
                return Pos(self.i, self.j - 1)

        raise RuntimeError(f"Unexpected dir: '{dir}'")

    def is_inside(self) -> bool:
        return self.i >= 0 and self.j >= 0 and self.i < N and self.j < N

with open("input") as file:
    N, P1_PREFIX = map(int, file.readline().split())
    WALLS = [Pos.parse(line) for line in file]

START = Pos(0, 0)
TARGET = Pos(N - 1, N - 1)

def bfs(prefix: int) -> Optional[int]:
    wset = set(WALLS[0:prefix])

    dist: dict[Pos, int] = {}
    dist[START] = 0

    queue = deque([START])

    while queue:
        cur = queue.popleft()
        cur_dist = dist[cur]

        if cur in wset:
            continue

        for dir in list('^>v<'):
            next = cur.step(dir)
            if (not next.is_inside()) or (next in wset) or (next in dist):
                continue

            dist[next] = cur_dist + 1

            if next == TARGET:
                return dist[next]

            queue.append(next)

    return None

# Solution (Part 1)
print("ans (p1):", bfs(P1_PREFIX))

# Solution (Part 2)
l = 0
r = len(WALLS)    
while l < r - 1:
    m = (l + r) // 2
    if bfs(m) == None:
        r = m
    else:
        l = m

pos = WALLS[r - 1]
print(f"ans (p2): {pos.i},{pos.j}")
