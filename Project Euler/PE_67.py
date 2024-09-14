with open("trangle.txt", 'r') as data_file:
    triangle_numbers = [[int(n) for n in line.split(" ")] for line in data_file]

for line in range(1, len(triangle_numbers)):
    for i in range(len(triangle_numbers[line])):
        last = len(triangle_numbers[line-1])
        triangle_numbers[line][i] += max(triangle_numbers[line-1][max(i-1,0):min(i+1, last)])

print(f'Solution to Project Euler Problem 18 is {max(triangle_numbers[-1])}')