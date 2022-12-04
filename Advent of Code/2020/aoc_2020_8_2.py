from dataclasses import dataclass
from pprint import pprint


class Op:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
        self.executed = False

    def execute(self):
        self.executed = True
        line_delta = 1
        acc_delta = 0

        if self.operator == "jmp":
            line_delta = self.operand
        elif self.operator == "acc":
            acc_delta = self.operand

        return line_delta, acc_delta

    def switch_operator(self):
        if self.operator == "nop":
            self.operator = "jmp"
        elif self.operator == "jmp":
            self.operator = "nop"

    def __repr__(self):
        return f'Op({self.operator=}, {self.operand=})'


@dataclass
class State:
    cmd: Op
    acc: int
    line: int

    def toggle_cmd(self):
        self.cmd.switch_operator()
        self.cmd.executed = False


def run(start_state):
    current_state = start_state
    program_run = []

    stop_run = False
    prog_finished = False

    while not stop_run:
        program_run.append(current_state)
        line_d, acc_d = current_state.cmd.execute()
        new_line = current_state.line + line_d
        new_acc = current_state.acc + acc_d
        if new_line > max(program.keys()):
            stop_run = True
            prog_finished = True
        else:
            new_opp = program[new_line]
            if new_opp.executed:
                stop_run = True
                prog_finished = False
            else:
                current_state = State(new_opp, new_acc, new_line)

    return prog_finished, program_run


# Main program
program = {}
with open("aoc_2020_8.txt", "r") as file:
    for i, command_line in enumerate(file, 1):
        op, opr = command_line.split(" ")
        program[i] = Op(op, int(opr.strip()))

res, orig_run = run(State(program[1], 0, 1))
new_run = orig_run

for state in reversed(orig_run):
    #     ss = state
    #     ss.toggle_cmd()
    #     print(ss)
    state.toggle_cmd()
    res, new_run = run(state)
    if res:
        break

print(f'Solution Part 2 is {new_run[-1].acc}')
