import re
from dataclasses import dataclass, field
from typing import Callable
from math import prod

with open("aoc_2022_11.txt") as file:
    file_contents = file.read()

starting_item_lines = re.findall(r'(?<=Starting items: )\d.*\d', file_contents)
operation_lines = re.findall(r'(?<=Operation: new = ).*', file_contents)
test_lines = re.findall(r'(?<=Test: ).*', file_contents)
true_lines = re.findall(r'(?<=If true: ).*', file_contents)
false_lines = re.findall(r'(?<=If false: ).*', file_contents)

problem = 2

@dataclass
class Monkey:
    items: list[int]
    operation: Callable = field(repr=False)
    test_value: int
    inspects: int = 0
    true_monkey: object = None
    false_monkey: object = None

    def round(self, monkey_list):
        while self.items:
            item = self.items.pop(0)
            self.inspects += 1
            item = self.operation(item)
            if problem == 1:
                item = item // 3
            else:
                item = item % div_product
            if item % self.test_value == 0:
                monkey_list[self.true_monkey].items.append(item)
            else:
                monkey_list[self.false_monkey].items.append(item)


@dataclass
class MonkeyTree:
    monkeys: list[Monkey] = field(default_factory=list)

    def round(self):
        for monkey in self.monkeys:
            monkey.round(self.monkeys)


monkey_tree = MonkeyTree()

for input_data in zip(starting_item_lines,
                      operation_lines,
                      test_lines,
                      ):
    item_list = [int(num) for num in re.findall(r'\d+', input_data[0])]
    op_func = eval(f"lambda x: {re.sub(r'old', 'x', input_data[1])}")
    test_val = int(re.search(r'\d+$', input_data[2]).group())
    monkey_tree.monkeys.append(Monkey(item_list, op_func, test_val))

for i, monkey_i in enumerate(monkey_tree.monkeys):
    monkey_i.true_monkey = int(re.search(r'\d+$', true_lines[i]).group())
    monkey_i.false_monkey = int(re.search(r'\d+$', false_lines[i]).group())

div_product = prod(mk.test_value for mk in monkey_tree.monkeys)

for _ in range(10_000):
    monkey_tree.round()

inspections = sorted([mk.inspects for mk in monkey_tree.monkeys], reverse=True)

print(f"Solution to problem is {inspections[0] * inspections[1]}")
