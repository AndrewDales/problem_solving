import re
from dataclasses import dataclass
from functools import lru_cache

with open("data/aoc_input_2023_12.txt") as file:
    file_contents = file.read()


class CanNotFit(Exception):
    pass


@dataclass(frozen=True)
class SpringPattern:
    symbols: str
    numbers: tuple[int, ...]

    @staticmethod
    def parse(sprint_tuple):
        syms = sprint_tuple[0]
        nums = tuple(int(n) for n in sprint_tuple[1].split(","))
        return SpringPattern(syms, nums)

    def shorten(self):
        n, nums = self.numbers[0], self.numbers[1:]
        if len(self.symbols) == n and '.' not in self.symbols:
            syms = ''
        elif len(self.symbols) > n and '.' not in self.symbols[:n] and not self.symbols[n] == '#':
            syms = '.' + self.symbols[n+1:]
        else:
            raise CanNotFit('No more room')
        return SpringPattern(syms, nums)

    def count_ways(self):
        # # no more numbers and no more '?' or '#', we have found the only way
        # if not self.numbers and self.symbols.count('?') + self.symbols.count('#'):
        #     count = 1
        # no more numbers, but '#' remain, impossible
        if not self.numbers and self.symbols.count('#') > 0:
            count = 0
        # numbers remain by no more symbols, impossible
        elif self.numbers and not self.symbols:
            count = 0
        # no more numbers only '.' or '?' remain
        elif not self.numbers and not '#' in self.symbols:
            count = 1
        # if pattern starts with '.', remove it
        elif self.symbols[0] == '.':
            count = SpringPattern(self.symbols[1:], self.numbers).count_ways()
        # if pattern starts with a '#' we must try to put the first number into the space
        elif self.symbols[0] == '#':
            try:
                count = self.shorten().count_ways()
            except CanNotFit:
                count = 0
        # if pattern starts with a '?' we can either put the first number in this position or remove the '?'
        else:
            count = SpringPattern(self.symbols[1:], self.numbers).count_ways()
            try:
                count = count + self.shorten().count_ways()
            except CanNotFit:
                pass

        return count

    def check_position(self, start=0, last=None):
        if last is None:
            last = len(self.symbols)
        valid_place = ((start == 0 or self.symbols[start-1] in '?.') and
                       (last == len(self.symbols) or self.symbols[last] in '?.') and
                       all(s in '#?' for s in self.symbols[start:last]))
        return valid_place

    def find_positions(self, n, min_start=0, max_last=None):
        if max_last is None:
            max_last = len(self.symbols)
        return [i for i in range(min_start, max_last - n + 1) if self.check_position(i, i + n)]

    @lru_cache
    def count_ways_bisect(self):
        if sum(self.numbers) < self.symbols.count('#') or (sum(self.numbers) >
                                                           self.symbols.count('#') + self.symbols.count('?')):
            num_ways = 0
        elif sum(self.numbers) == 0:
            num_ways = 1
        else:
            num_ways = 0
            mid_n = len(self.numbers) // 2
            mid_value = self.numbers[mid_n]
            lower_numbers = self.numbers[:mid_n]
            upper_numbers = self.numbers[mid_n+1:]
            middle_positions = self.find_positions(mid_value,
                                                   sum(lower_numbers) + len(lower_numbers),
                                                   len(self.symbols) - sum(upper_numbers) - len(upper_numbers)
                                                   )
            for mid_start in middle_positions:
                lower_symbols = self.symbols[:max(mid_start - 1, 0)]
                upper_symbols = self.symbols[mid_start+mid_value + 1:]
                num_ways += (SpringPattern(lower_symbols, lower_numbers).count_ways_bisect() *
                             SpringPattern(upper_symbols, upper_numbers).count_ways_bisect())
        return num_ways

    def expand(self):
        return SpringPattern('?'.join([self.symbols]*5), self.numbers*5)


file_matches = re.findall(r'([.#?]*) ([\d,]*)', file_contents)
springs = [SpringPattern.parse(fm) for fm in file_matches]
ways = [spring.count_ways() for spring in springs]

print(f'Solution to Day 12, Problem 1 is {sum(ways)}')

expanded_springs = [spring.expand() for spring in springs]

total_ways_expanded = sum(spring.count_ways_bisect() for spring in expanded_springs)

print(f'Solution to Day 12, Problem 1 is {total_ways_expanded}')
