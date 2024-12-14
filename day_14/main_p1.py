from dataclasses import dataclass
from functools import reduce
import operator
import re

@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: 'Vec2') -> 'Vec2':
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __mul__(self, m: int) -> 'Vec2':
        x = self.x * m
        y = self.y * m
        return Vec2(x, y)

    def wrapped(self) -> 'Vec2':
        x = self.x % W
        y = self.y % H
        return Vec2(x, y)

@dataclass(frozen=True)
class Robot:
    p: Vec2
    v: Vec2

    def forward(self, steps: int) -> 'Robot':
        return Robot(
            (self.p + self.v * steps).wrapped(),
            self.v
        )


LINE_RE = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')

robots = []

with open("input") as file:
    W, H = map(int, file.readline().split())

    for line in file:
        line = line.strip()
        m = LINE_RE.match(line)
        assert m
        p = Vec2(int(m.group(1)), int(m.group(2)))
        v = Vec2(int(m.group(3)), int(m.group(4)))
        robots.append(Robot(p, v))

robots_100 = list(map(lambda r: r.forward(100), robots))

positions = {}

for r in robots_100:
    if r.p not in positions:
        positions[r.p] = 0
    positions[r.p] += 1

MID_W = W // 2
MID_H = H // 2

# for i in range(H):
#     if i != MID_H:
#         for j in range(W):
#             v = Vec2(j, i)
#             if j != MID_W:
#                 if v in positions:
#                     print(positions[v], end='')
#                 else:
#                     print('.', end='')
#             else:
#                 print(' ', end='')
#     print()

quadrants = [0, 0, 0, 0]
for pos, count in positions.items():
    if pos.x == MID_W or pos.y == MID_H:
        continue

    quadrants[int(pos.y < MID_H) * 2 + int(pos.x < MID_W)] += count

# print(f"{quadrants}")

print("ans (p1):", reduce(operator.mul, quadrants, 1))



