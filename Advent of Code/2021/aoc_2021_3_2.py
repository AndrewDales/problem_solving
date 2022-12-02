def most_common_bit(bin_strings, col):
    col_sum = sum(int(bs[col]) for bs in bin_strings)
    return int(col_sum * 2 >= len(bin_strings))

def generator_rating(bin_strings, gas=None):
    n_cols = len(bin_strings[0])
    col = 0
    while len(bin_strings) > 1:
        mcb = most_common_bit(bin_strings, col)
        if gas == "CO2":
            mcb = 1 - mcb
        bin_strings = [bs for bs in bin_strings if bs[col] == str(mcb)]
        col += 1
    return int(bin_strings[0],2)
        

trial_input = ['00100',
                '11110',
                '10110',
                '10111',
                '10101',
                '01111',
                '00111',
                '11100',
                '10000',
                '11001',
                '00010',
                '01010',
               ]

with open("aoc_input_2021_3.txt", "r") as file:
    bin_input = [line.strip() for line in file]
    
o2 = generator_rating(bin_input, "O2")
co2 = generator_rating(bin_input, "CO2")

print(f'Output solution: {o2*co2}')
