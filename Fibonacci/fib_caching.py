import time
from functools import lru_cache
from math import sqrt
from decimal import Decimal
from decimal import *

@lru_cache(maxsize = 100000)
def fib(n):
    if n in (0,1):
        return n
    if n < 0:
        return fib(n+2)-fib(n+1)
    # Work out some values to put in cache
    if n > 50:
        for i in range(0,n,10):
            fib(i)
    return(fib(n-1)+fib(n-2))
    """Calculates the nth Fibonacci number"""

def fib_up(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a

def fib_form(n):
    n = Decimal(n)
    A = Decimal(sqrt(5)/5)
    lambda_1 = Decimal((1+sqrt(5))/2)
    lambda_2 = Decimal((1-sqrt(5))/2)
    return int(Decimal(A * (lambda_1 ** n - lambda_2 ** n)))

getcontext().prec = 1000
n = 20000
tic = time.perf_counter()
f_n = fib_form(n)
toc = time.perf_counter()
print(f"Found fib({n}) in {toc - tic:0.4f} seconds")
# print(f_n)
