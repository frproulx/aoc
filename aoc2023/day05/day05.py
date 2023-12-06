import argparse
import re
from aoc2023.utils import parse_file

class Mapper():
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        self.map_ranges = []

    def __repr__(self):
        return f"Map from {self.source} to {self.target}: {self.map_ranges}"
    
    def lookup_value(self, input_value):
        for map_range in self.map_ranges:
            if (input_value >= map_range[1]) and (input_value <= (map_range[1] + map_range[2])):
                return input_value + (map_range[0] - map_range[1])
        return input_value

class Payload():
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f'{self.type} (value={self.value})'
    
    def transform(self, maps):
        mapper = [map_ for map_ in maps if map_.source == self.type][0]
        return Payload(type=mapper.target, value=mapper.lookup_value(self.value))
    

def grow_plant(state, maps):
    while state.type != 'location':
        state = state.transform(maps)
    return state

def parse_maps(full_file):
    maps = []
    for row in full_file:
        if row.startswith('seeds:'):
            seeds = [Payload(type='seed', value=int(seed)) for seed in row.split(':')[1].strip().split(' ')]
            continue
        map_match = re.match('([A-Za-z]+)-to-([A-Za-z]+) map:', row)
        number_match = re.match('[0-9]+ [0-9]+ [0-9]+', row)
        if map_match:
            maps.append(Mapper(map_match.group(1), map_match.group(2)))
        elif number_match:
            maps[-1].map_ranges.append(tuple([int(i) for i in number_match.group().split(' ')]))
        else:
            continue
    return maps, seeds


def main(fi_name):
    input = parse_file(fi_name)
    maps, seeds = parse_maps(input)
    locations = [grow_plant(seed, maps) for seed in seeds]
    print(f"Lowest location: {min([l.value for l in locations])}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)