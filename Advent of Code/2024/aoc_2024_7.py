

with open('data/aoc_input_2024_7.txt') as file:
    file_contents = file.readlines()

test_values = []
operands = []

for line in file_contents:
    test, op_string = line.split(':')
    test_values.append(int(test))
    operands.append(tuple(map(int, op_string.strip().split(' '))))

def find_sums(operand_list):
    if len(operand_list) == 1:
        return operand_list
    else:
        val, operand_list = operand_list[-1], operand_list[:-1]
        return tuple(val + i for i in find_sums(operand_list)) + tuple(val * i for i in find_sums(operand_list))

def find_sum_cats(operand_list):
    if len(operand_list) == 1:
        return operand_list
    else:
        val, operand_list = operand_list[-1], operand_list[:-1]
        return (tuple(val + i for i in find_sum_cats(operand_list))
                + tuple(val * i for i in find_sum_cats(operand_list))
                + tuple(int(str(i) + str(val)) for i in find_sum_cats(operand_list))
                )

correct_tests = [test for test, op_list in zip(test_values, operands) if test in find_sums(op_list)]

print(f'Solution to Advent of Code Day 7a is {sum(correct_tests)}')

correct_tests = [test for test, op_list in zip(test_values, operands) if test in find_sum_cats(list(op_list))]

print(f'Solution to Advent of Code Day 7b is {sum(correct_tests)}')