from dataclasses import dataclass, field
import re
from aoc_2022_09 import add_vector, sub_vector

with open("aoc_2022_15.txt") as file:
    file_contents = file.read()

coord_pairs = re.findall(r'x=(-?[\d]+).*?y=(-?[\d]+)', file_contents)
coord_pairs = [(int(pair[0]), int(pair[1])) for pair in coord_pairs]


@dataclass(eq=True, frozen=True)
class Beacon:
    location: tuple[int, int]


@dataclass(eq=True, frozen=True)
class Sensor:
    location: tuple[int, int]
    beacon: Beacon = field(repr=False)

    @property
    def distance_to_beacon(self):
        diff = sub_vector(self.location, self.beacon.location)
        return abs(diff[0]) + abs(diff[1])

    def no_beacon_cells(self, row):
        x, y = self.location
        empty_on_row = set()
        if (num_on_row := abs(self.distance_to_beacon) - abs(row - y)) >= 0:
            empty_on_row = set((q, row) for q in range(x - num_on_row, x + num_on_row + 1))
        return empty_on_row

@dataclass
class AreaMap:
    locations: dict[tuple[int, int]: Sensor|Beacon] = field(default_factory=dict)
    sensors: set[Sensor] = field(default_factory=set, repr=False)
    beacons: set[Beacon] = field(default_factory=set, repr=False)

    @classmethod
    def parse_location_data(cls, location_list):
        area_map = AreaMap()
        for i in range(0, len(location_list), 2):
            beacon = Beacon(location_list[i+1])
            sensor = Sensor(location_list[i], beacon)
            area_map.sensors.add(sensor)
            area_map.beacons.add(beacon)
            area_map.locations[location_list[i]] = sensor
            area_map.locations[location_list[i+1]] = beacon
        return area_map

    def no_beacon_locations(self, row):
        locs = set()
        for snr in self.sensors:
            locs |= snr.no_beacon_cells(row)
        return locs


my_area_map = AreaMap.parse_location_data(coord_pairs)
no_beacons = my_area_map.no_beacon_locations(2_000_000)

print(f'Solution to Part 1 = {len(no_beacons)}')