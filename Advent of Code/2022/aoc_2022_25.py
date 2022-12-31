from bidict import bidict

with open("aoc_2022_25.txt") as file:
    snafu_data = [list(line.strip()) for line in file]

SNAFU_VALUES = bidict({'2': 2,
                       '1': 1,
                       '0': 0,
                       '-': -1,
                       '=': -2,
                       })


def snafu_sum(snafu_summands, carry=0):
    if not snafu_summands and carry == 0:
        return ''
    last_symbols = [summand.pop() for summand in snafu_summands]
    last_symbols_sum = sum(SNAFU_VALUES[sym] for sym in last_symbols) + carry
    carry, rem = divmod(last_symbols_sum, 5)
    if rem >= 3:
        rem -= 5
        carry += 1

    # Remove empty values from the list
    snafu_summands = [summand for summand in snafu_summands if summand]

    return snafu_sum(snafu_summands, carry) + SNAFU_VALUES.inverse[rem]


print(f'Solution to Day 25, problem 1 is {snafu_sum(snafu_data)}')
