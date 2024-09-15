# red must be the square root of triangular numbers that are also square.
# square triangular numbers are given by a recurrence relationship given in https://en.wikipedia.org/wiki/Square_triangular_number
# s_k is the sqrt of the kth square triangle number, and is a feasible number of red discs
from math import sqrt

square_triangular = [0, 1]

max_s_k = (10**12 // (2 + sqrt(2)))

while square_triangular[-1] < max_s_k:
    s_k = square_triangular[-1] * 6 - square_triangular[-2]
    square_triangular.append(s_k)

red = square_triangular[-1]
blue = (2 * red + 1 + int(sqrt(8* red **2 + 1))) // 2

assert blue / (blue + red) * (blue - 1) / (blue + red - 1) == 0.5

print(f'Solution to Project Euler number 100 is {blue}')