tri_numbers = set()
pent_numbers = set()
hex_numbers= set()
tri_number: int = 0

in_all_sets = 0

n = 1
while in_all_sets <= 2:
    tri_number = (n * (n + 1) // 2)
    pent_numbers.add(n * (3 * n - 1) // 2)
    hex_numbers.add(n * (2 * n - 1))
    tri_numbers.add(tri_number)
    if tri_number in hex_numbers and tri_number in pent_numbers:
        print(tri_number)
        in_all_sets += 1
    n += 1

print(f'Solution to Project Euler 45 is {tri_number}')