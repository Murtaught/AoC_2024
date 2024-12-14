from dataclasses import dataclass
from functools import reduce
import operator
import os
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

    def period(self) -> int:
        res = 1
        p = (self.p + self.v).wrapped()
        while p != self.p:
            res += 1
            p = (p + self.v).wrapped()
        return res

LINE_RE = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')

robots = []

with open("input") as file:
    W, H = map(int, file.readline().split())
    MID_W = W // 2
    MID_H = H // 2

    for line in file:
        line = line.strip()
        m = LINE_RE.match(line)
        assert m
        p = Vec2(int(m.group(1)), int(m.group(2)))
        v = Vec2(int(m.group(3)), int(m.group(4)))
        robots.append(Robot(p, v))

def compute_positions(robots):
    positions = {}
    for r in robots:
        if r.p not in positions:
            positions[r.p] = 0
        positions[r.p] += 1
    return positions

def show_robots(second, robots):
    positions = compute_positions(robots)
    os.system('clear')
    print(f"After {second} seconds:")
    for y in range(H):
        for x in range(W):
            v = Vec2(x, y)
            if v in positions:
                print('#', end='')
            else:
                print('.', end='')
        print()

period = None
for r in robots:
    cur_per = r.period()
    if period == None:
        period = cur_per
    else:
        assert cur_per == period

print(f"All robots have the same period: {period}")

def contains_frame(robots):
    poss = set()
    for r in robots:
        poss.add(r.p)

    lines = []
    for y in range(H):
        x0 = None
        for x in range(W + 1):
            if Vec2(x, y) in poss:
                if x0 == None:
                    x0 = x
            else:
                if x0 != None and x - x0 >= 30:
                    lines.append((y, x0, x))
                x0 = None

    return len(lines) >= 2

for seconds_passed in range(period):
    if contains_frame(robots):
        print("ans (p2):", seconds_passed)
        break

    robots = list(map(lambda r: r.forward(1), robots))
