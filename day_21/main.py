from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import Optional, Tuple, Callable, Generator
import functools

class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def reverse(self) -> Dir:
        match self:
            case Dir.N: return Dir.S
            case Dir.E: return Dir.W
            case Dir.S: return Dir.N
            case Dir.W: return Dir.E
        raise RuntimeError(f"Unexpected Dir value: {self}.")

    def arrow(self) -> str:
        match self:
            case Dir.N: return '^'
            case Dir.E: return '>'
            case Dir.S: return 'v'
            case Dir.W: return '<'
        raise RuntimeError(f"Unexpected Dir value: {self}.")

    def __repr__(self) -> str:
        return self.arrow()



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

Char = str
Path = str
CharMatrix = list[list[Char]]

class Keypad:
    mtx: CharMatrix

    def __init__(self, repr: str):
        self.mtx = [list(line.strip()) for line in repr.splitlines()]

    def show(self) -> None:
        for row in self.mtx:
            print(''.join(row))

    def height(self) -> int:
        return len(self.mtx)

    def width(self) -> int:
        return len(self.mtx[0])

    def get(self, pos: Pos) -> Optional[Char]:
        if pos.i < 0 or pos.j < 0 or pos.i >= self.height() or pos.j >= self.width():
            return None
        return self.mtx[pos.i][pos.j]

    def is_forbidden(self, pos: Pos) -> bool:
        return self.get(pos) == '#'

    def find(self, c: Char) -> Optional[Pos]:
        for pos in self.all_positions():
            if self.get(pos) == c:
                return pos
        return None

    def all_positions(self) -> Generator[Pos, None, None]:
        for i in range(self.height()):
            for j in range(self.width()):
                yield Pos(i, j)

    # @functools.cache
    def bfs(self, start: Pos, dirs: list[Dir]) -> dict[Pos, Optional[Dir]]:
        dir_taken: dict[Pos, Optional[Dir]] = {start: None}
        queue = deque([start])

        while queue:
            cur = queue.popleft()
            
            for dir in dirs:
                next = cur.step(dir)
                if (next in dir_taken) or (self.get(next) in [None, '#']):
                    continue

                dir_taken[next] = dir
                queue.append(next)

        return dir_taken

    def shortest_path(self, frm: Char, to: Char, dirs: list[Dir]) -> Path:
        start = self.find(frm)
        assert start
        finish = self.find(to)
        assert finish

        dir_taken = self.bfs(start, dirs)

        def restore_path(pos: Pos) -> str:
            ret = []
            while dir := dir_taken.get(pos):
                ret.append(dir)
                pos = pos.step(dir.reverse())

            return ''.join(map(Dir.arrow, ret[::-1]))

        return restore_path(finish)

    def wrap(self, buttons: str, dirs: list[Dir]) -> str:
        ret = ''
        cur = 'A'
        for b in list(buttons):
            ret += self.shortest_path(cur, b, dirs)
            ret += 'A'
            cur = b
        return ret

    def all_wraps(self, buttons: str) -> set[str]:
        wraps = set(self.wrap(buttons, dirs) for dirs in DIR_PERMS)
        n = min(len(w) for w in wraps)
        return set(filter(lambda w: len(w) == n, wraps))


NUM_KP = Keypad("789\n456\n123\n#0A")
DIR_KP = Keypad("#^A\n<v>")
DIR_PERMS = list(map(list, permutations([Dir.N, Dir.E, Dir.S, Dir.W])))

with open("input") as file:
    inputs = [line.strip() for line in file]

TRANSITIONS: dict[Char, dict[Char, list[str]]] = {
    '^': {
        'A': ['>'],
        '<': ['v<'],
        'v': ['v'],
        '>': ['v>', '>v'],
    },
    'A': {
        '^': ['<'],
        '<': ['<v<', 'v<<'],
        'v': ['<v', 'v<'],
        '>': ['v'],
    },
    '<': {
        '^': ['>^'],
        'A': ['>>^', '>^>'],
        'v': ['>'],
        '>': ['>>'],
    },
    'v': {
        '^': ['^'],
        'A': ['^>', '>^'],
        '<': ['<'],
        '>': ['>'],
    },
    '>': {
        '^': ['^<', '<^'],
        'A': ['^'],
        '<': ['<<'],
        'v': ['<'],
    },
}

@functools.cache
def rec(s: str, depth: int) -> int:
    if depth < 0:
        return len(s)

    p = 'A'
    ret = 0
    for c in list(s):
        if c != p:
            ret += min((rec(trans + 'A', depth - 1) for trans in TRANSITIONS[p][c]))
        else:
            ret += rec('A', depth - 1)
        p = c

    return ret

def solve(input: str, depth: int) -> int:
    wraps = NUM_KP.all_wraps(input)
    length = min(rec(wrap, depth) for wrap in wraps)
    number = int(input.replace('A', ''))
    return number * length

print("ans (p1):", sum(solve(input,  1) for input in inputs))
print("ans (p2):", sum(solve(input, 24) for input in inputs))
