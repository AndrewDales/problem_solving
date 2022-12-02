with open("aoc_input_2021_8.txt", "r") as file:
    signal_patterns = []
    output_values = []
    for line in file:
        signal_pattern, output_value = line.strip().split("|")
        signal_patterns.append(signal_pattern.strip().split(" "))
        output_values.append(output_value.strip().split(" "))

unique_digits = {2: 1, 4: 4, 3: 7, 7: 8}

output_uniques = [sum(True for el in row if len(el) in unique_digits) for row in output_values]

print(f'Output Solution Part 1: {sum(output_uniques)}')

output_numbers = []
for signal_display, output in zip(signal_patterns, output_values):
#signal_display, output = signal_patterns[0], output_values[0]
    signal_display.sort(key=len)
    signal_dict = {}
    for pattern in signal_display:
        if (l:= len(pattern)) in unique_digits:
            signal_dict[unique_digits[l]] = pattern
        elif len(pattern) == 5:
            # It's a 3
            if len(set(signal_dict[1]) & set(pattern)) == 2:
                signal_dict[3] = pattern
            # It's a 2
            elif len(set(signal_dict[4]) & set(pattern)) == 2:
                signal_dict[2] = pattern
            # It's a 5    
            else:
                signal_dict[5] = pattern
        elif len(pattern) == 6:
            # It's a 6
            if len(set(signal_dict[1]) & set(pattern)) == 1:
                signal_dict[6] = pattern
            # It's a 9
            elif len(set(signal_dict[4]) & set(pattern)) == 4:
                signal_dict[9] = pattern
            # It's a 0
            else:
                signal_dict[0] = pattern

    inv_signal_dict = {frozenset(v): k for k, v in signal_dict.items()}
    output_num = "".join([str(inv_signal_dict[frozenset(code)]) for code in output])
    output_numbers.append(int(output_num))

print(f'Output Solution Part 2: {sum(output_numbers)}')