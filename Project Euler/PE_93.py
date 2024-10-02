import operator
import itertools

operations = (operator.add, operator.sub, operator.mul, operator.truediv)
op_perms = list(itertools.product(operations, repeat=3))
num_combos = list(itertools.combinations(range(1, 10), 4))
rpn_sequences = ('nnnnooo', 'nnnonoo', 'nnnoono', 'nnonnoo', 'nnonono')


def calc_rpn(num_combo, op_perm, rpn_sequence):
    num_stack = []
    operands = iter(num_combo)
    operators = iter(op_perm)

    try:
        for op_type in rpn_sequence:
            if op_type == 'n':
                num_stack.append(next(operands))
            if op_type == 'o':
                b = num_stack.pop()
                a = num_stack.pop()
                num_stack.append(next(operators)(a, b))
    except ZeroDivisionError:
        output = -1
    else:
        output = num_stack.pop()

    return output


def calc_all_results(num_combo):
    pos_values = set(int(val)
                     for op_perm in op_perms
                     for rpn_sequence in rpn_sequences
                     for nums in itertools.permutations(num_combo)
                     if (val := calc_rpn(nums, op_perm, rpn_sequence)) > 0 and val % 1 == 0)
    return pos_values


def sequence_length(values):
    n = 0
    while n + 1 in values:
        n += 1
    return n


max_length = 0
max_combo = (1, 2, 3, 4)
for i, combo in enumerate(num_combos):
    if (n := sequence_length(calc_all_results(combo))) > max_length:
        max_length = n
        max_combo = list(combo)
    #
    # if i % 1000:
    #     print(f'{i / len(num_combos):.2f}')

max_combo.sort()

print(f'Solution to Project Euler 93 is {max_combo[0]}{max_combo[1]}{max_combo[2]}{max_combo[3]}')
