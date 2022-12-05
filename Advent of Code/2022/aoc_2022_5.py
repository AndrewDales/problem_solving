import re
from collections import defaultdict, namedtuple

with open("aoc_2022_5.txt") as file:
    raw_data = file.readlines()

stacks = defaultdict(list)
moves = []
Move = namedtuple('Move',['number', 'start', 'end'])
prob = 2

blank_line = raw_data.index('\n')
head = reversed(raw_data[:blank_line])
move_data = raw_data[blank_line+1:]

header = next(head)
head_match = re.finditer(r'[0-9]', header)
head_start = [hd.start() for hd in head_match]

while True:
    try:
        stack_list = next(head)
        for i, val in enumerate(head_start, 1):
            if not stack_list[val].isspace():
                stacks[i].append(stack_list[val])
    except StopIteration:
        break

for line in move_data:
    moves.append(Move(*[int(num) for num in re.findall(r'[0-9]+', line)]))

for move in moves:
    if prob == 1:
        for _ in range(move.number):
            stacks[move.end].append(stacks[move.start].pop())
    if prob == 2:
        move_items = stacks[move.start][-move.number:]
        del stacks[move.start][-move.number:]
        stacks[move.end].extend(move_items)


solution = "".join(stack[-1] for stack in stacks.values())
print(solution)