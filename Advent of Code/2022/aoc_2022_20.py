with open("aoc_2022_20.txt") as file:
    number_list = [int(line.strip()) for line in file]

DECRYPT_KEY = 811589153


def shift_value(p_list, val):
    val_index = p_list.index(val)
    p_list.remove(val)
    new_index = (val_index + val[0]) % len(p_list)
    if new_index == 0 and val[0] < 0:
        p_list.append(val)
    else:
        p_list.insert(new_index, val)


def mix(code_list, num_times):
    new_list = code_list.copy()
    for _ in range(num_times):
        for el in code_list:
            shift_value(new_list, el)
            # print(new_list)
    return new_list


def find_vals_after_zero(p_list):
    zero_pos = p_list.index(0)
    vals = [p_list[(zero_pos + 1000) % len(p_list)],
            p_list[(zero_pos + 2000) % len(p_list)],
            p_list[(zero_pos + 3000) % len(p_list)],
            ]
    print(vals)
    return sum(vals)


number_list_tuples = [(el, i) for i, el in enumerate(number_list)]

mixed_list_tuples = mix(code_list=number_list_tuples, num_times=1)
mixed_list = [el[0] for el in mixed_list_tuples]
print(f'Solution to part 1: {find_vals_after_zero(mixed_list)}')

code_list_2 = [(el * DECRYPT_KEY, i) for i, el in enumerate(number_list)]

mixed_list_tuples_2 = mix(code_list=code_list_2, num_times=10)
mixed_list_2 = [el[0] for el in mixed_list_tuples_2]

print(f'Solution to part 1: {find_vals_after_zero(mixed_list_2)}')