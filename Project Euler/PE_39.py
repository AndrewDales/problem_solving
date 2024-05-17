import math
from collections import defaultdict

perimeter_count = defaultdict(int)

# Create primitive prime triples
p_prime_triples = [(m ** 2 - n ** 2, 2 * m * n, m ** 2 + n ** 2)
                   for n in range(1, 25)
                   for m in range(n + 1, 26)
                   if not (n % 2 == 1 and m % 2 == 1) and math.gcd(n, m) == 1
                   ]

perimeters = [sum(pt) for pt in p_prime_triples]

for p in perimeters:
    for a in range(1, 1000 // p + 1):
        perimeter_count[a*p] += 1

print(f'Solution to Project Euler 39 is {max(perimeter_count, key=perimeter_count.get)}')