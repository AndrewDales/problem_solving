from math import factorial

# Take 1 off the target number to account for counting the first element as index 0
target = 1_000_000-1
digits = list('0123456789')
answer = ''

for i in range(len(digits)-1, -1, -1):
    n_digit, target = divmod(target, factorial(i))
    next_digit = digits[n_digit]
    digits.remove(next_digit)
    answer += next_digit

print(answer)




