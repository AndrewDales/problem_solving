from collections import namedtuple

with open("aoc_2022_10.txt") as file:
    raw_data = [line.strip().split(" ") for line in file]
    prog_data = [cmd if len(cmd) == 1 else (cmd[0], int(cmd[1])) for cmd in raw_data]

RegState = namedtuple("RegState", ['start', 'end'])


class Execution:
    def __init__(self, register_value: int = 1):
        self.state_dict = {}
        self.state = 0
        self.initial_register = 1

    def execute_command(self, opcode: str, operand: int | None = None):
        try:
            reg_x = self.state_dict[self.state].end
        except KeyError:
            reg_x = self.initial_register

        if opcode == "noop":
            self.state += 1
            self.state_dict.update({self.state: RegState(reg_x, reg_x)})

        elif opcode == "addx":
            self.state_dict.update({self.state + 1: RegState(reg_x, reg_x),
                                    self.state + 2: RegState(reg_x, reg_x + operand),
                                    })
            self.state += 2

    def execute_program(self, prog):
        for instruction in prog:
            self.execute_command(*instruction)

    def calc_strength(self):
        return sum(i * self.state_dict[i].start for i in range(20, 221, 40))


class CRT:
    sprites_per_line = 40

    def __init__(self):
        self.sprite_pos = range(0, 3)
        self.lines = [[]]
        self.current_line = self.lines[-1]
        self.current_pixel = 0

    def cycle(self, reg_state: RegState):
        if self.current_pixel in self.sprite_pos:
            self.current_line.append('█')
        else:
            self.current_line.append(" ")
        self.sprite_pos = range(reg_state.end - 1, reg_state.end + 2)
        self.current_pixel += 1
        if self.current_pixel >= self.sprites_per_line :
            self.lines.append([])
            self.current_line = self.lines[-1]
            self.current_pixel = self.current_pixel % self.sprites_per_line

    def run_execution(self, p_exec: Execution):
        for i in range(1, len(p_exec.state_dict) + 1):
            self.cycle(p_exec.state_dict[i])

    def show(self):
        for line in self.lines:
            print("".join(line))

my_exec = Execution()
my_exec.execute_program(prog_data)

print(f"Solution to part 1 is {my_exec.calc_strength()}")

my_crt = CRT()
my_crt.run_execution(my_exec)
my_crt.show()
