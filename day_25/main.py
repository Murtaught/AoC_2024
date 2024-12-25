from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import cast, Generator, Iterable
import copy
import re

N = 7
M = 5

Pins = list[int]

locks: list[Pins] = []
keys:  list[Pins] = []

buffer: list[str] = []

def process_buffer() -> None:
    global buffer
    global locks
    global keys

    if not buffer:
        return

    n = len(buffer)
    m = len(buffer[0])
    assert n == N
    assert m == M

    # print('\n'.join(buffer))
    # print("lock" if buffer[0][0] == '#' else "key")
    out_list = locks if buffer[0][0] == '#' else keys

    pins: Pins = [ sum(1 for i in range(n) if buffer[i][j] == '#') - 1 for j in range(m) ]
    # print(pins, '\n')

    out_list.append(pins)
    buffer = []


with open("input") as file:
    for line in file:
        line = line.strip()
        if line == '':
            process_buffer()
        else:
            buffer.append(line)
    process_buffer()


print("locks:", len(locks))
print("keys: ", len(keys))


def are_compatible(a: Pins, b: Pins) -> bool:
    return all([sum(p) <= (N - 2) for p in zip(a, b)])

ans_p1 = 0
for lock in locks:
    for key in keys:
        if are_compatible(lock, key):
            ans_p1 += 1

print("ans (p1):", ans_p1)
