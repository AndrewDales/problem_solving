from functools import lru_cache
import time

@lru_cache(maxsize=None)
def collatz_chain(n: int):
    if n == 1:
        chain = [1,]
    elif n % 2 == 0:
        chain = collatz_chain(n // 2).copy()
        chain.append(n)
    else:
        chain = collatz_chain(3 * n + 1).copy()
        chain.append(n)
    return chain

tic = time.time()
print(max(range(1, 1_000_001), key=lambda x: len(collatz_chain(x))))
toc = time.time()

print(f'Time taken = {toc - tic:0.4f} seconds')

# collatz_list = ((len(collatz_chain(i)), i) for i in range(1,1000))
# collatz_chain(1001)

# @lru_cache(maxsize=None)
# def collatz_chain(n: int):
#     if n == 1:
#         chain = (1,)
#     elif n % 2 == 0:
#         # chain = collatz_chain(n // 2).copy()
#         chain = collatz_chain(n // 2,) + (n,)
#     else:
#         # chain = collatz_chain(3 * n + 1).copy()
#         chain = collatz_chain(3 * n + 1) + (n,)
#     return chain