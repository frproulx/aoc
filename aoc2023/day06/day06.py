import argparse
import re
from math import sqrt, ceil, floor, prod
from aoc2023.utils import parse_file

def get_margin(t, d):
    sqrt_term = sqrt(t*t - 4*d) - 1e-8
    min_ta = (t - sqrt_term)/2
    max_ta = (t + sqrt_term)/2
    print(min_ta, max_ta)
    return floor(max_ta) - ceil(min_ta) + 1

def get_numerics(line):
    return [int(x) for x in re.findall('[0-9]+', line)]

def main(fi_name):
    input = parse_file(fi_name)
    for row in input:
        if row.startswith("Time:"):
            times = get_numerics(row)
        elif row.startswith("Distance:"):
            dists = get_numerics(row)
        else:
            raise ValueError("Bad input!")
    margins = [get_margin(t, d) for t, d in zip(times, dists)]
    print(margins)
    print(f"Round 1: total margin: {prod(margins)}")

    t_2 = int(''.join([str(t) for t in times]))
    d_2 = int(''.join([str(d) for d in dists]))
    round2_margin = get_margin(t_2, d_2)
    print(f"Round2 total margin: {round2_margin}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)