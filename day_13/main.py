import re
import sympy as sp
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def solve(a: Point, b: Point, target: Point) -> int:
    # print(f"Solving A = {a}, B = {b}, Prize at {target} ... ", end = '')

    i, j = sp.symbols("i, j", integer = True)
    symbols = [i, j]
    equations = [
        sp.Eq( i * a.x + j * b.x, target.x ),
        sp.Eq( i * a.y + j * b.y, target.y ),
    ]

    best = None
    solutions = sp.solve(equations, *symbols, dict=True)
    for no, sol in enumerate(solutions):
        ans = sol[i] * 3 + sol[j]
        if best:
            best = min(ans, best)
        else:
            best = ans

    # print(f"best = {best}")
    return best or 0


BUTTON_RE = re.compile(r'^Button (A|B): X\+(\d+), Y\+(\d+)$')
PRIZE_RE  = re.compile(r'^Prize: X=(\d+), Y=(\d+)$')

BUMP = 10000000000000

def bumped(p: Point) -> Point:
    return Point(p.x + BUMP, p.y + BUMP)

ans_p1 = 0
ans_p2 = 0

with open("input") as file:
    a = b = target = None
    for line in file:
        line = line.strip()
        if m := BUTTON_RE.match(line):
            p = Point(int(m.group(2)), int(m.group(3)))
            if m.group(1) == 'A':
                a = p
            else:
                b = p

        elif m := PRIZE_RE.match(line):
            target = Point(int(m.group(1)), int(m.group(2)))

        else:
            assert line == ''
            ans_p1 += solve(a, b, target)
            ans_p2 += solve(a, b, bumped(target))
            a = b = target = None

    if target != None:
        ans_p1 += solve(a, b, target)
        ans_p2 += solve(a, b, bumped(target))


print('ans (p1):', ans_p1)
print('ans (p2):', ans_p2)


