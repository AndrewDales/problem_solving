import re

with open("data/aoc_input_2023_1.txt") as file:
    file_contents = file.readlines()

def word_int(d_string: str) -> int | None:
    num = None
    if d_string.isdigit():
        num = int(d_string)
    elif d_string in number_words:
        num = number_words[d_string]
    return str(num)


digits = [re.findall(r'\d', line) for line in file_contents]
numbers = [int(digit[0] + digit[-1]) for digit in digits]

print(f'Solution to Day 1, part 1 is {sum(numbers)}')

number_words = {'one': 1,
                'two': 2,
                'three': 3,
                'four': 4,
                'five': 5,
                'six': 6,
                'seven': 7,
                'eight': 8,
                'nine': 9,
                }

number_words_str = rf'(\d|{"|".join(number_words)})'
# This uses a lookahead regex - see https://mtsknn.fi/blog/how-to-do-overlapping-matches-with-regular-expressions/
number_pattern = re.compile(rf'(?={number_words_str})')
digits_and_words = [number_pattern.findall(line) for line in file_contents]
numbers = [int(word_int(digit[0]) + word_int(digit[-1])) for digit in digits_and_words]

print(f'Solution to Day 1, part 2 is {sum(numbers)}')
