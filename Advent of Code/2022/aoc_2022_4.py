import re


def parse_line(p_line):
    number_strings = re.findall(r'[0-9]+', p_line)
    return sorted([(int(number_strings[0]), int(number_strings[1])),
                   (int(number_strings[2]), int(number_strings[3]))],
                  )


with open("aoc_2022_4.txt", "r") as file:
    range_data = [parse_line(line) for line in file]

num_contained = sum(1 for r_1, r_2 in range_data if (r_1[0] == r_2[0]) or (r_2[1] <= r_1[1]))
num_overlap = sum(1 for r_1, r_2 in range_data if r_1[1] >= r_2[0])

print(f'Solution Part 1 is {num_contained}')
print(f'Solution Part 1 is {num_overlap}')
