import operator as op

with open("data/aoc_input_2019_2.txt", "r") as file:
    line = file.readline()
    numbers_orig = [num for num in line.strip().split(",")]


def gravity_assist():
    numbers = numbers_orig.copy()

    stop_prog = False
    pointer = 0

    while not stop_prog:
        op_num = numbers[pointer]
        if len(op_num) >= 4:
            op_num = f'{op_num:>5}'
            op_code = int(op_num[-1])
            immediate = [bool(n) for n in reversed(op_num[:3])]


        if op_code in (1, 2):
            parameters = numbers[pointer+1: pointer+4]

        elif op_num == 99:
            stop_prog = True

    return numbers[0]