import re
from operator import itemgetter

with open("data/aoc_input_2023_5.txt") as file:
    file_contents = file.read()

chunks = file_contents.split(':')


class MapRanges:
    def __init__(self, map_list):
        map_triples = [map_list[i:i + 3] for i in range(0, len(map_list), 3)]
        self.source_ranges = [range(map_triple[1], map_triple[1] + map_triple[2]) for map_triple in map_triples]
        self.dest_ranges = [range(map_triple[0], map_triple[0] + map_triple[2]) for map_triple in map_triples]

    def map_value(self, source_value):
        for source_range, dest_range in zip(self.source_ranges, self.dest_ranges):
            if source_value in source_range:
                source_pos = source_range.index(source_value)
                dest_value = dest_range[source_pos]
                break
        else:
            dest_value = source_value
            source_range = None
        return dest_value, source_range

    def map_value_list(self, source_list):
        return [self.map_value(i)[0] for i in source_list]

    def map_range(self, p_range):
        dest_start, source_range = self.map_value(p_range.start)

        if source_range is None:
            higher_source_ranges = [s_range for s_range in self.source_ranges if s_range.start > p_range.stop]
            low_higher_source_range = []
            if higher_source_ranges:
                low_higher_source_range = min(higher_source_ranges, key=itemgetter(0))

            if not low_higher_source_range:
                dest_ranges = [p_range]
            else:
                range_end = low_higher_source_range.start
                if range_end in p_range:
                    cut = p_range.index(range_end)
                    dest_ranges = [p_range[:cut]] + self.map_range(p_range[cut:])
                else:
                    dest_ranges = [p_range]
        else:
            if p_range.stop in source_range:
                dest_ranges = [range(dest_start,
                                     self.map_value(p_range.stop - 1)[0] + 1)]
            else:
                dest_ranges = [range(dest_start,
                                     self.map_value(source_range.stop - 1)[0] + 1)] + self.map_range(
                    range(source_range.stop, p_range.stop))

        return dest_ranges

    def map_range_list(self, source_ranges):
        new_ranges = []
        for source_range in source_ranges:
            new_ranges += self.map_range(source_range)
        return new_ranges


seeds = [int(n) for n in re.findall(r'\d+', chunks[1])]
maps = [[int(n) for n in re.findall(r'\d+', chunk)] for chunk in chunks[2:]]
mappings = [MapRanges(map_list) for map_list in maps]

source = seeds

for current_map in mappings:
    source = current_map.map_value_list(source)

print(f'Solution to Day 5, Part 1 is {min(source)}')

seed_ranges = [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

for current_map in mappings:
    seed_ranges = current_map.map_range_list(seed_ranges)

print(f'Solution to Day 5, Part 2 is {min(rng.start for rng in seed_ranges)}')
