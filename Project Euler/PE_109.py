from numpy import convolve

singles = [0] * 61
doubles = [0] * 61
triples = [0] * 61

for i in range(1, 21):
    singles[i] = 1
    doubles[i * 2] = 1
    triples[i * 3] = 1

singles[25] = 1
doubles[50] = 1

# Number of ways of throwing each number with one throw
one_throw = [sum(x) for x in zip(singles, doubles, triples)]

two_out = list(convolve(one_throw, doubles))

# two_repeat - ways of throwing two of the same number
two_repeat = [0] * 121
for i, val in enumerate(one_throw):
    if val > 0:
        two_repeat[i * 2] = val

# two_throw - ways of throwing two darts
two_throw = list(convolve(one_throw, one_throw))

# adjust to so that throw 1 then throw 2 is the same as throw 2 then throw 1 (if the two throws are different)
two_throw = [x - y for x, y in zip(two_throw, two_repeat)]
two_throw = [i // 2 for i in two_throw]
two_throw = [sum(x) for x in zip(two_throw, two_repeat)]

three_out = convolve(two_throw, doubles)

co_below_100 = sum(three_out[:100]) + sum(two_out[:100]) + sum(doubles[:100])

print(f'Number of ways of checking out with less than score less than 100 = {co_below_100}')
