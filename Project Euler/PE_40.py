from math import prod

champernownes_constant = ''

for i in range(1, 1_000_000 // 5):
    champernownes_constant += str(i)

digits = [int(champernownes_constant[i-1]) for i in [1, 10, 100, 1000, 10_000, 100_000, 1_000_000]]

print(f'Solution to Project Euler 40 is {prod(digits)}')
