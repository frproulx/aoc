import argparse
import re
from itertools import combinations
from aoc2023.utils import parse_file

def number_group_combos(groups, numbers):
    full_row = '.'.join(groups)
    
    total_numbers = sum(numbers)
    total_known_locations = sum([x == '#' for x in full_row])
    total_to_assign = total_numbers - total_known_locations
    if total_numbers < total_known_locations:
        print(full_row, numbers)
    question_spots = [m.start() for m in re.finditer('\?', full_row)]
    arrangement_count = 0
    for replaceables in combinations(question_spots, total_to_assign):
        candidate = list(full_row)
        for i in replaceables:
            candidate[i] = '#'
        candidate_str = ''.join(candidate)
        if validate_arrangement(candidate_str, numbers):
            arrangement_count += 1
    return arrangement_count


def validate_arrangement(arrangement, numbers):
    return [len(q) for q in re.findall('#+', arrangement)] == numbers

def main(fi_name):
    inputs = parse_file(fi_name)
    total_arrangements = 0
    for row in inputs:
        location_groups = re.findall('[?#]+', row)
        numbers = [int(i) for i in re.findall('[0-9]+', row)]
        total_arrangements += number_group_combos(location_groups, numbers)
    print(f"{total_arrangements} Total arrangements")

    total_arrangements_2 = 0
    for row in inputs:
        gear_map = row.split(' ')[0]
        expanded_row = '?'.join([gear_map for _ in range(5)])
        location_groups = re.findall('[?#]+', expanded_row)
        numbers = [int(i) for i in re.findall('[0-9]+', row)]
        full_numbers = []
        for _ in range(5):
            full_numbers.extend(numbers)
        total_arrangements_2 += number_group_combos(location_groups, full_numbers)
    print(f"{total_arrangements_2} Part 2: Total arrangements")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)