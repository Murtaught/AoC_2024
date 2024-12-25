from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import cast, Generator, Iterable, Optional
import copy
import re
import random

INPUT_RE = re.compile(r'^(\w+): (0|1)$')
GATE_RE = re.compile(r'^(\w+) (AND|OR|XOR) (\w+) -> (\w+)$')

class Op(Enum):
    AND = 1
    OR  = 2
    XOR = 3

    def perform(self, a: bool, b: bool) -> bool:
        match self:
            case Op.AND: return a and b
            case Op.OR:  return a  or b
            case Op.XOR: return a   ^ b
        raise RuntimeError(f"Unexpected Op value: {self}")

    def symbol(self) -> str:
        match self:
            case Op.AND: return '&'
            case Op.OR:  return '|'
            case Op.XOR: return '^'
        raise RuntimeError(f"Unexpected Op value: {self}")


@dataclass
class Gate:
    name: str
    op: Op
    lhs: str
    rhs: str


inputs: dict[str, bool] = {}
gates:  dict[str, Gate] = {}

with open("input-fixed") as file:
    for line in file:
        line = line.strip()
        if m := INPUT_RE.match(line):
            inputs[m.group(1)] = (m.group(2) != '0')
        elif m := GATE_RE.match(line):
            lhs  = m.group(1)
            op   = Op[m.group(2)]
            rhs  = m.group(3)
            name = m.group(4)

            if lhs > rhs:
                lhs, rhs = rhs, lhs

            gates[name] = Gate(name, op, lhs, rhs)


MAX_NUM = (1 << 44) - 1

def decode_and_set(x: int, prefix: str, values: dict[str, bool]) -> None:
    for index in range(45):
        values[f'{prefix}{index:02}'] = bool(x & 1)
        x = x >> 1

def get(name: str, values: dict[str, bool]) -> bool:
    if name not in values:
        assert name in gates
        gate = gates[name]
        lhs = get(gate.lhs, values)
        rhs = get(gate.rhs, values)
        values[name] = gate.op.perform(lhs, rhs)
    return values[name]

def run(x: int, y: int) -> int:
    assert x <= MAX_NUM
    assert y <= MAX_NUM

    values: dict[str, bool] = {}
    decode_and_set(x, 'x', values)
    decode_and_set(y, 'y', values)

    z = 0
    for index in range(45, -1, -1):
        z = (z << 1) + int(get(f'z{index:02}', values))

    return z


tests_ran = 0
while True:
    x = random.randint(0, MAX_NUM)
    y = random.randint(0, MAX_NUM)
    z = run(x, y)
    if z != (x + y):
        print(f"Failed at {x} + {y} = {z} (instead of {x + y}, which is correct)")
        print(f"x  = _{x:044b}")
        print(f"y  = _{y:044b}")
        print(f"z  = {z:045b}")
        print(f"c. = {x + y:045b}")
        break

    tests_ran += 1
    if tests_ran % 10_000 == 0:
        print(tests_ran, 'tests ran ...')
