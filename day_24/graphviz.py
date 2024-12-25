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


# Let's generate a graph using GraphViz.
xs = list(f'x{i:02}' for i in range(45))
ys = list(f'y{i:02}' for i in range(45))
zs = list(f'z{i:02}' for i in range(45 + 1))

inout = set(xs) | set(ys) | set(zs)

with open("graph.dot", 'w') as out:
    out.write("digraph G { \n")
    out.write('  rankdir="TB";');

    out.write("node [shape=plaintext, fontcolor=red, fontsize=18];")
    out.write('"X:" -> "Y:" -> "Z:" [color=white];');


    out.write("  node [shape=record, fontcolor=black, fontsize=14, width=25, fixedsize=true];");

    label = ' | '.join(map(lambda x: f"<{x}> {x}", xs))
    out.write(f'  xs [label="{label}", color=blue, fillcolor=lightblue, style=filled]; \n')

    label = ' | '.join(map(lambda y: f"<{y}> {y}", ys))
    out.write(f'  ys [label="{label}", color=red, fillcolor=lightpink, style=filled]; \n')

    label = ' | '.join(map(lambda z: f"<{z}> {z}", zs))
    out.write(f'  zs [label="{label}", color=yellow2, fillcolor=lightyellow, style=filled]; \n')

    def wrap(name: str) -> str:
        if name in inout:
            return f'{name[0]}s:{name}'
        return name

    out.write('  edge [color=black]; \n')
    out.write("  node [shape=square, fontcolor=black, fontsize=14, width=0.5, fixedsize=true, color=magenta, fillcolor=lightskyblue, style=filled]; \n")
    for gate in gates.values():
        if gate.name in inout:
            continue

        out.write(f'  {gate.name} [label="{gate.op.symbol()}"]; \n')
        out.write(f'  {wrap(gate.lhs)} -> {gate.name}; \n')
        out.write(f'  {wrap(gate.rhs)} -> {gate.name}; \n')

    for z in zs:
        gate = gates[z]
        out.write(f'  {gate.name} [label="{gate.op.symbol()}"]; \n')
        out.write(f'  {wrap(gate.lhs)} -> {gate.name}; \n')
        out.write(f'  {wrap(gate.rhs)} -> {gate.name}; \n')
        out.write(f'  {gate.name} -> {wrap(z)}; \n')


    out.write('  { rank=same; "X:"; xs } \n')
    out.write('  { rank=same; "Y:"; ys } \n')
    out.write('  { rank=same; "Z:"; zs } \n')


    out.write('} \n')
