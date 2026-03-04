# 1 to 20
numbers = {1: 'one',
           2: 'two',
           3: 'three',
           4: 'four',
           5: 'five',
           6: 'six',
           7: 'seven',
           8: 'eight',
           9: 'nine',
           10: 'ten',
           11: 'eleven',
           12: 'twelve',
           13: 'thirteen',
           14: 'fourteen',
           15: 'fifteen',
           16: 'sixteen',
           17: 'seventeen',
           18: 'eighteen',
           19: 'nineteen',
           }

tens = {20: 'twenty',
        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety',
        }

# 20 to 99
for i in range(20, 100):
    t, u = divmod(i, 10)
    if u == 0:
        numbers[i] = tens[t * 10]
    else:
        numbers[i] = f'{tens[t * 10]} {numbers[u]}'

# 100 to 999
for i in range(1, 10):
    numbers[i * 100] = numbers[i] + ' hundred'
    for j in range(1, 100):
        numbers[i * 100 + j] = numbers[i * 100] + ' and ' + numbers[j]

numbers[1000] = 'one thousand'

answer = sum(len(number.replace(" ", "")) for number in numbers.values())

print(f'Solution to Project Euler Problem 17 is {answer}')