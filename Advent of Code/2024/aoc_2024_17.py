from dataclasses import dataclass, field
import re
from typing import Optional

file_contents = """Register A: 61156655
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,4,3,1,6,0,3,5,5,3,0"""

# file_contents = """Register A: 729
# Register B: 0
# Register C: 0
#
# Program: 0,1,5,4,3,0"""

# file_contents = """Register A: 117440
# Register B: 0
# Register C: 0
#
# Program: 0,3,5,4,3,0"""

register_str = re.findall(r'[ABC]:\s(\d+)', file_contents)
program_str = re.findall(r'Program:\s([\d,]+)', file_contents)
program_nums = [int(num) for num in program_str[0].split(',')]

@dataclass
class Computer:
    registers: dict[str: int] = field(default_factory=dict)
    cir: int = 0
    output: list[str] = field(default_factory=list)

    def get_combo_operand(self, c_operand: int) -> int:
        value = None
        if 0 <= c_operand < 4:
            value = c_operand
        elif c_operand == 4:
            value = self.registers['A']
        elif c_operand == 5:
            value = self.registers['B']
        elif c_operand == 6:
            value = self.registers['C']
        return value

    def execute(self, cmd: "Instruction"):
        cmd.c_operand = self.get_combo_operand(cmd.operand)
        match cmd.opcode:
            # (adv) division - shift right
            case 0:
                self.registers['A'] = self.registers['A'] >> cmd.c_operand
            # (bxl) bitwise XOR B and operand
            case 1:
                self.registers['B'] = self.registers['B'] ^ cmd.operand
            # (bst) modulo 8
            case 2:
                self.registers['B'] = cmd.c_operand & 7
            # (jnz) jump non-zero
            case 3:
                if self.registers['A'] != 0:
                    self.cir = cmd.operand - 1
            # (bxc) bitwise XOR B and C
            case 4:
                self.registers['B'] = self.registers['B'] ^ self.registers['C']
            # (out) output combo operand mod 8
            case 5:
                self.output.append(str(cmd.c_operand & 7))
                # print(cmd.c_operand & 7)
            # (bdv) division - shift right store in B
            case 6:
                self.registers['B'] = self.registers['A'] >> cmd.c_operand
            # (cdv) division - shift right store in C
            case 7:
                self.registers['C'] = self.registers['A'] >> cmd.c_operand

        self.cir += 1


    def run(self, program):
        while 0 <= self.cir < len(program):
            self.execute(program[self.cir])

@dataclass
class Instruction:
    opcode: int
    operand: int
    c_operand: Optional[int] = None

def out(a):
    x = (a % 8) ^ 5
    y = a >> x
    z = x ^ 6
    return (y ^ z) % 8


computer = Computer({'A': int(register_str[0]), 'B': int(register_str[1]), 'C': int(register_str[2])})
instructions = tuple(Instruction(program_nums[i], program_nums[i+1]) for i in range(0,len(program_nums),2))

# computer.registers['A'] = 105734774294938
computer.run(instructions)

print(f'Solution to Day 17a is {','.join(computer.output)}')


rqd_outputs = program_nums[::-1]
valid_inputs = [0]

for rqd_output in rqd_outputs:
    valid_inputs = [(start_val << 3) + i for i in range(8) for start_val in valid_inputs
                     if out((start_val << 3) + i) == rqd_output]

print(f'Solution to Day 17b is {min(valid_inputs)}')