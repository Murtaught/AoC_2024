from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import cast, Generator, Iterable
import copy
import re

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

@dataclass
class Gate:
    name: str
    op: Op
    lhs: str
    rhs: str

inputs: dict[str, bool] = {}
gates:  dict[str, Gate] = {}

with open("input") as file:
    for line in file:
        line = line.strip()
        if m := INPUT_RE.match(line):
            inputs[m.group(1)] = (m.group(2) != '0')
        elif m := GATE_RE.match(line):
            lhs  = m.group(1)
            op   = Op[m.group(2)]
            rhs  = m.group(3)
            name = m.group(4)
            gates[name] = Gate(name, op, lhs, rhs)

# Solution (Part 1)
values = copy.deepcopy(inputs)

def get(name: str) -> bool:
    if name not in values:
        assert name in gates
        gate = gates[name]
        lhs = get(gate.lhs)
        rhs = get(gate.rhs)
        values[name] = gate.op.perform(lhs, rhs)

    return values[name]


bits = ''
for z_idx in range(100):
    z = f'z{z_idx:02}'
    if z in gates:
        bits = str(int(get(z))) + bits
    else:
        break

print("ans (p1):", int(bits, 2))
