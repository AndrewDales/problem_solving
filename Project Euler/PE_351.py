import time

from utilities import euler_totient, phi_sieve


MAX_N = 100_000_000
H = 0
phi_vals = phi_sieve(MAX_N)

tic = time.perf_counter()
H = sum(i + 1 - phi_vals[i] for i in range(1, MAX_N))

toc = time.perf_counter()
print(H * 6)
print(toc - tic)