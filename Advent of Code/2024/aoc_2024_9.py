from dataclasses import dataclass, field
from collections import OrderedDict
# from typing import OrderedDict

# file_contents = "2333133121414131402"
#
with open('data/aoc_input_2024_9.txt') as file:
    file_contents = file.read().strip()


@dataclass
class Memory:
    files: OrderedDict[int, int] = field(default_factory=OrderedDict)
    gaps: list[int] = field(default_factory=list)

    def set_up(self, file_string):
        self.files = OrderedDict((i, int(val))for i, val in enumerate(file_string[::2]))
        self.gaps = list(map(int, file_string[1::2]))

    def de_frag(self):
        compact_memory = []
        while self.files:
            # Fill files
            top_file = self.files.popitem(last=False)
            compact_memory += [top_file[0]]* top_file[1]

            # Fill gaps
            gap = self.gaps.pop(0)
            while gap and self.files:
                file_num, file_size = self.files.popitem()
                if gap >= file_size:
                    compact_memory += [file_num] * file_size
                    gap -= file_size
                else:
                    compact_memory += [file_num] * gap
                    self.files[file_num] = file_size - gap
                    gap = 0
        return compact_memory

@dataclass
class MemoryChunk:
    files: OrderedDict[int, tuple[int, int]] = field(default_factory=OrderedDict)
    gaps: list[tuple[int, int]] = field(default_factory=list)
    de_fragged_files: dict[int, tuple[int, int]] = field(default_factory=dict)

    def set_up(self, file_string):
        location = 0
        for i, val in enumerate(file_string):
            if i % 2 == 0:
                self.files[i//2] = (location, location + int(val))
            else:
                self.gaps.append((location, location + int(val)))
            location += int(val)

    def find_gap(self, min_size, max_index):
        for i, gap in enumerate(self.gaps):
            gap_size = gap[1] - gap[0]
            if gap_size >= min_size:
                return gap, i
            if gap[0] >= max_index:
                break
        return None, None

    def de_frag(self):
        while self.files:
            # Take a file from the end
            file_num, file_pos = self.files.popitem()
            file_size = file_pos[1] - file_pos[0]
            gap, pos = self.find_gap(file_size, file_pos[0])
            # if no gap is found leave the file where it is
            if gap is None:
                self.de_fragged_files[file_num] = file_pos
            # else move the file into the gap and reduce the size of the gap
            else:
                self.de_fragged_files[file_num] = (gap[0], gap[0] + file_size)
                self.gaps[pos] = (gap[0] + file_size, gap[1])

    def find_check_sum(self):
        return sum(sum(range(*pos)) * memory_id for memory_id, pos in self.de_fragged_files.items())

memory = Memory()
memory.set_up(file_contents)
com_mem = memory.de_frag()

checksum = sum(i * int(val) for i, val in enumerate(com_mem))

print(f'Solution to Advent of Code Day 9a is {checksum}')

memory = MemoryChunk()
memory.set_up(file_contents)
memory.de_frag()

print(f'Solution to Advent of Code Day 9b is {memory.find_check_sum()}')