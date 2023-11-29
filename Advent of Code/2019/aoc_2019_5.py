import operator as op

with open("data/aoc_input_2019_2.txt", "r") as file:
    line = file.readline()
    numbers_orig = [int(num) for num in line.strip().split(",")]

# Set up opcodes
opcodes = {1: op.add,
           2: op.mul,
           }


def gravity_assist():
    numbers = numbers_orig.copy()
    numbers[1] = 2
    numbers[2] = 12

    stop_prog = False
    pointer = 0

    while not stop_prog:
        op_num = numbers[pointer]
        if len(str(op_num)) >= 4:
            op_num = f'{op_num:>5}'
            op_code = int(op_num[-1])
            immediate = [bool(n) for n in reversed(op_num[:3])]
        else:
            op_code = int(op_num)
            immediate = [False] * 3

        if op_code in (1, 2):
            parameters = numbers[pointer + 1: pointer + 4]
            *operands, out_ad = [prm if add else int(numbers[prm]) for prm, add in zip(parameters, immediate)]
            numbers[out_ad] = opcodes[op_code](*operands)
            pointer += 4

        elif op_code == 99:
            stop_prog = True

    return numbers[0]


print(f'Solution to Day 2, problem 1 is {gravity_assist()}')
