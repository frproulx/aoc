import argparse
import re
from aoc2023.utils import parse_file

class Mapper():
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        # map ranges are dest start, source start, and length
        self.map_ranges = []

    def __repr__(self):
        return f"Map from {self.source} to {self.target}: {self.map_ranges}"
    
    def lookup_value(self, input_value):
        for map_dest, map_source, map_len in self.map_ranges:
            if (input_value >= map_source) and (input_value < (map_source + map_len)):
                return input_value + (map_dest - map_source)
        return input_value
    
    def map_range_of_values(self, range_start, range_end):
        break_points = [range_start, range_end]
        for _, map_source, map_len in self.map_ranges:
            for bp in [map_source, map_source + map_len]:
                if (bp > range_start) and (bp < range_end):
                    break_points += [bp]
        sorted_break_points = sorted(list(set(break_points)))
        dest_ranges = []
        n_breaks = len(sorted_break_points)
        for i in range(n_breaks - 1):
            if i < n_breaks - 2:
                dest_range = [
                    self.lookup_value(sorted_break_points[i]),
                    self.lookup_value(sorted_break_points[i + 1] - 1)
                ]
            else:
                dest_range = [
                    self.lookup_value(sorted_break_points[i]),
                    self.lookup_value(sorted_break_points[i + 1])
                ]
            if dest_range[1] >= dest_range[0]:
                dest_ranges.append(dest_range)
        return dest_ranges


class Payload():
    def __init__(self, state, value):
        self.state = state
        self.value = value
    
    def __repr__(self):
        return f'{self.state} (value={self.value})'
    
    def transform(self, maps):
        mapper = [map_ for map_ in maps if map_.source == self.state][0]
        return Payload(state=mapper.target, value=mapper.lookup_value(self.value))
    

class RangesOfPlants():
    def __init__(self, state, ranges):
        self.state = state
        self.ranges = ranges

    def __repr__(self) -> str:
        return f'{self.state} ({self.ranges})'

    def transform(self, maps):
        mapper = [map_ for map_ in maps if map_.source == self.state][0]
        new_ranges = []
        for range in self.ranges:
            new_ranges += mapper.map_range_of_values(*range)
        return RangesOfPlants(state=mapper.target, ranges=new_ranges)
    

def grow_plant(plant, maps):
    while plant.state != 'location':
        print(plant.state)
        if isinstance(plant, RangesOfPlants):
            print(min(l[0] for l in plant.ranges))
        plant = plant.transform(maps)
    print(plant.state)
    if isinstance(plant, RangesOfPlants):
        print(min(l[0] for l in plant.ranges))
    return plant

def parse_maps(full_file):
    maps = []
    for row in full_file:
        if row.startswith('seeds:'):
            seed_vals = [int(s) for s in row.split(':')[1].strip().split(' ')]
            seeds = [Payload(state='seed', value=seed) for seed in seed_vals]
            seed_val_ranges = [(seed_vals[2*i], seed_vals[2*i] + seed_vals[2*i + 1]) for i in range(int(len(seed_vals) / 2))]
            seed_ranges = RangesOfPlants(state='seed', ranges=seed_val_ranges)
            continue
        map_match = re.match('([A-Za-z]+)-to-([A-Za-z]+) map:', row)
        number_match = re.match('[0-9]+ [0-9]+ [0-9]+', row)
        if map_match:
            maps.append(Mapper(map_match.group(1), map_match.group(2)))
        elif number_match:
            maps[-1].map_ranges.append(tuple([int(i) for i in number_match.group().split(' ')]))
        else:
            continue
    return maps, seeds, seed_ranges

def main(fi_name):
    input = parse_file(fi_name)
    maps, seeds, seed_ranges = parse_maps(input)
    locations = [grow_plant(seed, maps) for seed in seeds]
    print(f"Lowest location: {min([l.value for l in locations])}")

    location_ranges = grow_plant(seed_ranges, maps)
    print(f"Lowest location from ranges: {min([l[0] for l in location_ranges.ranges])}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)