from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
import re


REGISTER_RE = re.compile(r'^Register (A|B|C): (-?\d+)$')
PROGRAM_RE = re.compile(r'^Program: ((?:[0-7],?)+)$')

class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

@dataclass(frozen=True)
class Instr:
    op: Opcode
    arg: int

def parse_program(bytes: list[int]) -> list[Instr]:
    res: list[Instr] = []
    cur: Optional[Opcode] = None

    for byte in bytes:
        if cur != None:
            assert cur
            res.append(Instr(cur, byte))
            cur = None
        else:
            cur = Opcode(byte)

    assert cur == None
    return res

class Interpreter:
    registers: dict[str, int]
    program: list[Instr]
    program_bytes: list[int]
    iidx: int = 0
    outputs: list[int] = []

    def __init__(self, registers: dict[str, int], program: list[int]):
        self.registers = registers
        self.program_bytes = program
        self.program = parse_program(program)

    @staticmethod
    def read_file(filename: str) -> Interpreter:
        with open(filename) as file:
            registers: dict[str, int] = {}
            program: list[int] = []

            for line in file:
                line = line.strip()
                if m := REGISTER_RE.match(line):
                    registers[m.group(1)] = int(m.group(2))

                elif m := PROGRAM_RE.match(line):
                    program = list(map(int, m.group(1).split(',')))
                    
            return Interpreter(registers, program)

    def is_finished(self) -> bool:
        return self.iidx < 0 or self.iidx >= len(self.program)

    def reset(self, a_value: int) -> None:
        self.registers['A'] = a_value
        self.registers['B'] = 0
        self.registers['C'] = 0
        self.iidx = 0
        self.outputs = []

    def combo(self, value: int) -> int:
        assert value >= 0
        assert value <= 6

        if value <= 3:
            return value

        match value:
            case 4: return self.registers['A']
            case 5: return self.registers['B']
            case 6: return self.registers['C']

        assert False

    def step(self) -> None:
        if self.is_finished():
            return

        cur = self.program[self.iidx]
        next_idx: int = self.iidx + 1

        match cur.op:
            case Opcode.ADV:
                self.registers['A'] //= (2 ** self.combo(cur.arg))

            case Opcode.BXL:
                self.registers['B'] ^= cur.arg

            case Opcode.BST:
                self.registers['B'] = self.combo(cur.arg) % 8

            case Opcode.JNZ:
                if self.registers['A'] != 0:
                    assert cur.arg % 2 == 0
                    next_idx = cur.arg // 2

            case Opcode.BXC:
                self.registers['B'] ^= self.registers['C']

            case Opcode.OUT:
                self.outputs.append(self.combo(cur.arg) % 8)

            case Opcode.BDV:
                self.registers['B'] = self.registers['A'] // (2 ** self.combo(cur.arg))

            case Opcode.CDV:
                self.registers['C'] = self.registers['A'] // (2 ** self.combo(cur.arg))

        self.iidx = next_idx

    def run(self) -> None:
        while not self.is_finished():
            self.step()


interp = Interpreter.read_file("input")

interp.run()
print("ans (p1):", ','.join(map(str, interp.outputs)))

cur_a = 0
while True:
    interp.reset(cur_a)
    interp.run()
    if interp.outputs == interp.program_bytes:
        print("ans (p2):", cur_a)
        break

    if cur_a % 10_000_000 == 0:
        print(cur_a, '...')

    cur_a += 1
