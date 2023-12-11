import argparse
import re
from aoc2023.utils import parse_file

EXPANSION = 1_000_000

def distance_calc(x1, y1, x2, y2, empty_rows, empty_cols):
    base_distance = abs(y2-y1) + abs(x2-x1)
    row_expansion = sum([(r > min(y1, y2)) and (r < max(y1, y2)) for r in empty_rows])
    col_expansion = sum([(c > min(x1, x2)) and (c < max(x1, x2)) for c in empty_cols])
    return base_distance + ((EXPANSION-1) * row_expansion) + ((EXPANSION - 1) * col_expansion)

def main(fi_name):
    galaxy_locations = {}
    input = parse_file(fi_name)
    empty_cols = []
    all_cols = set()
    empty_cols = [x for x in range(len(input[0]))]
    for j, row in enumerate(input):
        col_locs = [m.start() for m in re.finditer('#', row)]
        galaxy_locations[j] = col_locs
        all_cols = all_cols.union(set(col_locs))
    empty_rows = [j for j, vals in galaxy_locations.items() if vals == []]
    empty_cols = [c for c in range(0, max(all_cols)) if c not in all_cols]

    all_galaxies = []
    for j, i_list in galaxy_locations.items():
        all_galaxies.extend([(i ,j) for i in i_list])
    distances = [
        distance_calc(*a, *b, empty_rows=empty_rows, empty_cols=empty_cols) 
        for idx, a in enumerate(all_galaxies) for b in all_galaxies[idx + 1:]]

    print(f"Total distance: {sum(distances)}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)