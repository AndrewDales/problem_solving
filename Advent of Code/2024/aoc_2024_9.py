from dataclasses import dataclass, field
from collections import OrderedDict
# from typing import OrderedDict

# file_contents = "2333133121414131402"

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
    gaps: list[int] = field(default_factory=list)

    def set_up(self, file_string):
        memory_index = 0
        location = 0
        for val in file_string:
            self.files[memory_index] = (location, location + int(val))


memory = Memory()
memory.set_up(file_contents)
com_mem = memory.de_frag()

checksum = sum(i * int(val) for i, val in enumerate(com_mem))

print(f'Solution to Advent of Code Day 9a is {checksum}')