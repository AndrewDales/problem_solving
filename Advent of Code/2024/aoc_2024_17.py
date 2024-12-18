from dataclasses import dataclass, field
import re

file_contents = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

register_str = re.findall(r'[ABC]:\s(\d+)', file_contents)
program_str = re.findall(r'Progam: ([\d])')

@dataclass
class Computer:
    registers: dict[str: int] = field(default_factory=dict)


@dataclass
class Instruction:
    opcode: int
    operand: int