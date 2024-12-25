from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import cast, Generator, Iterable, Optional
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

    def symbol(self) -> str:
        match self:
            case Op.AND: return '&'
            case Op.OR:  return '|'
            case Op.XOR: return '^'
        raise RuntimeError(f"Unexpected Op value: {self}")


@dataclass
class Gate:
    name: str
    comment: str
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

            if lhs > rhs:
                lhs, rhs = rhs, lhs

            gates[name] = Gate(name, '', op, lhs, rhs)


unused: dict[str, Gate] = {}
for k, v in gates.items():
    unused[k] = v

consumers: dict[str, set[str]] = defaultdict(lambda: set())
for gate in gates.values():
    consumers[gate.lhs].add(gate.name)
    consumers[gate.rhs].add(gate.name)

N = 45

def var_name(letter: str, i: int) -> str:
    assert letter in 'xyz'
    return f"{letter}{i:02}"

def find_gate(a: str, b: str, op: Op) -> Optional[Gate]:
    if a > b:
        a, b = b, a
    for gate in gates.values():
        if gate.lhs == a and gate.rhs == b and gate.op == op:
            return gate
    return None

def definitely(smth: Optional[Gate]) -> Gate:
    assert smth
    return smth


xor1_by_index: dict[int, Gate] = {}
and1_by_index: dict[int, Gate] = {}
zs: dict[int, Gate] = {}
carries: dict[int, Gate] = {}

for i in range(N):
    # XOR-1 and AND-1
    # (these are all good)
    x = var_name('x', i)
    y = var_name('y', i)
    
    xor1 = definitely(find_gate(x, y, Op.XOR))
    xor1.comment = f"xor1-{i:02}"
    xor1_by_index[i] = xor1
    unused.pop(xor1.name)

    assert xor1.name == 'z00' or not xor1.name.startswith('z')

    and1 = definitely(find_gate(x, y, Op.AND))
    and1.comment = f"and1-{i:02}"
    and1_by_index[i] = and1
    unused.pop(and1.name)

    # Outputs
    z = var_name('z', i)
    if z in unused:
        z_gate = unused[z]
        if z_gate.op == Op.XOR:
            zs[i] = z_gate
            unused.pop(z)
    else:
        if z == 'z00':
            # LSB is a special case.
            assert i == 0
            zs[0] = xor1_by_index[0]
        else:
            print(f"{z} is missing")

# LSB is a special case.
carries[0] = and1_by_index[0]
for i in range(1, N):
    and1 = and1_by_index[i]
    xor1 = xor1_by_index[i]
    prev = carries[i - 1]
    
    and2 = find_gate(xor1.name, prev.name, Op.AND)
    if not and2:
        print(f"Failed to find AND-2 for index {i}!")
        print(f"xor1 = {xor1}, prev = {prev}")
        print(f"xor1's consumers = {consumers[xor1.name]}")
        print(f"prev's consumers = {consumers[prev.name]}")
        break
    unused.pop(and2.name)

    cur = find_gate(and1.name, and2.name, Op.OR)
    if not cur:
        print(f"Failed to find carry for index {i}!")
        break
    unused.pop(cur.name)

    carries[i] = cur

print("wsv: ", gates['wsv'])
print(len(unused))

# But wait...
for gate in gates.values():
    if gate.op != Op.XOR:
        continue

    if gate.comment.startswith('xor1'):
        continue

    if gate.name.startswith('z'):
        continue

    print(gate)
    print(' ', gates[gate.lhs])
    print(' ', gates[gate.rhs])

# All AND gates must have only one consumer (except AND1-00, which is the same as CARRY-00)
for gate in gates.values():
    if gate.op != Op.AND:
        continue

    cons = consumers[gate.name]
    if len(cons) == 1:
        continue

    if gate == and1_by_index[00]:
        continue

    print(f"Suspicious gate: {gate} | {cons}")

