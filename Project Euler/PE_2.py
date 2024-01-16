fib_sequence =[1, 1]

while fib_sequence[-1] < 4_000_000:
    fib_sequence.append(fib_sequence[-2] + fib_sequence[-1])
    
print(sum(f for f in fib_sequence[:-1] if f % 2 ==0))