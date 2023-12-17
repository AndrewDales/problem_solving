from dataclasses import dataclass
from collections import defaultdict

with open("data/aoc_input_2023_15.txt") as file:
    file_contents = file.read()

file_contents = file_contents.strip()
instructions = file_contents.split(sep=',')


@dataclass(frozen=True)
class Instruct:
    label: str
    type: str
    focal: int | None = None

    @property
    def box(self):
        return aoc_hash(self.label)

    def find_in_box(self):
        places = [i for i, instruction in enumerate(boxes[self.box]) if instruction.label == self.label]
        if places:
            return places[0]
        else:
            return None

    def implement_instruction(self):
        instruct_position = self.find_in_box()
        if self.type == "-" and instruct_position is not None:
            boxes[self.box].pop(instruct_position)
        elif self.type == "=":
            if instruct_position is None:
                boxes[self.box].append(self)
            else:
                boxes[self.box][instruct_position] = self


def aoc_hash(p_string: str):
    current_value = 0
    for char in p_string:
        current_value += ord(char)
        current_value = current_value * 17 % 256
    return current_value


def parse_instruction(p_instruction):
    if '=' in p_instruction:
        instruct = p_instruction.split('=')
        instruct = Instruct(label=instruct[0], type='=', focal=int(instruct[1]))
    else:
        instruct = Instruct(label=p_instruction[:-1], type='-')
    return instruct


def focusing_power(box_number, box_contents):
    fp = sum((1 + box_number) * i * instruction.focal for i, instruction in enumerate(box_contents, 1))
    return fp


hashed_instructions = [aoc_hash(instruction) for instruction in instructions]
print(f'Solution to Day 15, part 1 is {sum(hashed_instructions)}')

instructions = [parse_instruction(instruction) for instruction in instructions]
boxes = defaultdict(list)

for instruction in instructions:
    instruction.implement_instruction()

focusing_powers = [focusing_power(i, contents) for i, contents in boxes.items()]

print(f'Solutino to Day 15, part 2 is {sum(focusing_powers)}')
