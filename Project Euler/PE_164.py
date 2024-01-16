from collections import defaultdict

class LowSumNumber:
    def __init__(self):
        self.n_digits = 3
        self.last_3_digits = {(i, j, k) : 0
                              for i in range(10)
                              for j in range(10)
                              for k in range(10)
                              if i + j + k <= 9}
        for i, j, k in self.last_3_digits:
            if i > 0:
                self.last_3_digits[(i, j, k)] = 1
    
    
    @property
    def total(self):
        return sum(self.last_3_digits.values())
    
    def add_digit(self):
        self.n_digits += 1
        new_digit_counts = defaultdict(int)
        for digit_tuple in self.last_3_digits:
            for i in range(10 - sum(digit_tuple[1:])):
                new_tuple = digit_tuple[1:] + (i, )
                new_digit_counts[new_tuple] += self.last_3_digits[digit_tuple]
        self.last_3_digits = new_digit_counts
        
    def total_n_digits(self, n):
        while self.n_digits < n:
            self.add_digit()
        return self.total
        
        
n = 20

low_sum_number = LowSumNumber()
low_sum_number.add_digit()

print(f'Total number of {n} digit numbers with no three digits having sum greater than 9 = {low_sum_number.total_n_digits(n)}')

# test
# count = 0
# for i in range(10_000, 100_000):
#     s = str(i)
#     d = [int(n) for n in s]
#     if sum(d[:3]) <=9 and sum(d[1:4]) <= 9 and sum(d[2:]) <= 9:
#         count+=1
# print(count)