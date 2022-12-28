import re
from dataclasses import dataclass

with open("aoc_2022_21.txt") as file:
    file_contents = file.read()

leaf_data = re.findall(r'([a-z]{4}):\s(\d+)', file_contents)
tree_data = re.findall(r'([a-z]{4}):\s([a-z]{4})\s([+-/*])\s([a-z]{4})', file_contents)


@dataclass
class MonkeyNode:
    name: str
    value: float | str | None = None
    op_symbol: str | None = None
    children: tuple[str, str] | None = None

    def __post_init__(self):
        if self.op_symbol == "+":
            self.operation = lambda x, y: x.__add__(y)
        elif self.op_symbol == "-":
            self.operation = lambda x, y: x.__sub__(y)
        elif self.op_symbol == "*":
            self.operation = lambda x, y: x.__mul__(y)
        elif self.op_symbol == "/":
            self.operation = lambda x, y: x.__floordiv__(y)

    def find_value(self):
        if self.value is None:
            node_1 = NODE_DIR[self.children[0]]
            node_2 = NODE_DIR[self.children[1]]
            val_1 = node_1.find_value()
            val_2 = node_2.find_value()
            if val_1 == "unknown" or val_2 == "unknown":
                result = "unknown"
            else:
                result = self.operation(val_1, val_2)
            self.value = result
            # print(f'{val_1} {self.op_symbol} {val_2} = {result}')
        else:
            result = self.value
        return result

    def back_fill(self):
        if self.children is None:
            return self

        value = self.value
        child_nodes = [NODE_DIR[self.children[0]], NODE_DIR[self.children[1]]]
        if child_nodes[0].value == "unknown":
            unknown = 0
        elif child_nodes[1].value == "unknown":
            unknown = 1
        else:
            raise ValueError("Neither child is unknown")

        if self.op_symbol == "+":
            child_nodes[unknown].value = value - child_nodes[1 - unknown].value
        elif self.op_symbol == "-" and unknown == 0:
            child_nodes[0].value = value + child_nodes[1].value
        elif self.op_symbol == "-" and unknown == 1:
            child_nodes[1].value = child_nodes[0].value - value
        elif self.op_symbol == "*":
            child_nodes[unknown].value = value // child_nodes[1 - unknown].value
        elif self.op_symbol == "/" and unknown == 0:
            child_nodes[0].value = value * child_nodes[1].value
        elif self.op_symbol == "/" and unknown == 1:
            child_nodes[1].value = child_nodes[0].value // value
        elif self.op_symbol == "=":
            child_nodes[unknown].value = child_nodes[1 - unknown].value

        # print(child_nodes[unknown].name, child_nodes[unknown].value)
        child_nodes[unknown].back_fill()


NODE_DIR = {ld[0]: MonkeyNode(ld[0], int(ld[1])) for ld in leaf_data} \
            | {td[0]: MonkeyNode(td[0],
                                 op_symbol=td[2],
                                 children=(td[1], td[3]))
               for td in tree_data}

root = NODE_DIR["root"]
root_value = root.find_value()

print(f'Solution to Day 21, part 1 is {root_value}')

NODE_DIR = {ld[0]: MonkeyNode(ld[0], int(ld[1])) for ld in leaf_data} \
            | {td[0]: MonkeyNode(td[0],
                                 op_symbol=td[2],
                                 children=(td[1], td[3]))
               for td in tree_data}

humn_node = NODE_DIR['humn']
humn_node.value = "unknown"

root = NODE_DIR["root"]
root_value = root.find_value()
root.op_symbol = "="

xx = root.back_fill()

print(f'Solution to Day 21, part 1 is {humn_node.value}')
