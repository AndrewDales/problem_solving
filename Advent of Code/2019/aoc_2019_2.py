import operator as op

with open("aoc_input_2019_2.txt", "r") as file:
    line = file.readline()
    numbers_orig = [int(num) for num in line.strip().split(",")]

# Set up opcodes
opcodes = {1: op.add,
           2: op.mul,
           }


def gravity_assist(noun, verb):
    numbers = numbers_orig.copy()
    numbers[1] = noun
    numbers[2] = verb

    stop_prog = False
    pointer = 0

    while not stop_prog:
        if (op_num := numbers[pointer]) in opcodes:
            addresses = numbers[pointer+1: pointer+4]
            result = opcodes[op_num](numbers[addresses[0]], numbers[addresses[1]])
            numbers[addresses[2]] = result
            pointer += 4
        elif op_num == 99:
            stop_prog = True

    return numbers[0]


def find_inputs():
    for i in range(100):
        for j in range(100):
            res = gravity_assist(i, j)
            if res == 19690720:
                return i, j


print(f'Solution to Day 2, problem 1 is {gravity_assist(12, 2)}')
a, b = find_inputs()
print(f'Solution ot Day 2, problem 2 is {a*100 + b}')
