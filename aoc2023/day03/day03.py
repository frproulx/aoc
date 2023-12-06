import argparse
import re
from collections import defaultdict
from aoc2023.utils import parse_file

def get_symbol_locations(grid):
    symbol_locs = defaultdict(list)
    for i, row in enumerate(grid):
        symbol_matches = re.finditer('[^.0-9]', row)
        for symbol in symbol_matches:
            symbol_locs[i].append(symbol.start())
    return symbol_locs

def get_numbers(grid):
    for i, row in enumerate(grid):
        number_matches = re.finditer('[0-9]+', row)
        for number in number_matches:
            yield (number.group(0), i, number.start())

def check_number(number, symbols):
    val, i, j_i = number
    val_length = len(val)
    ret_val = 0
    for i_delta in range(-1, 2):
        symbol_row = symbols.get(i + i_delta, [])
        if any([(j >= (j_i - 1)) and (j <= j_i + val_length) for j in symbol_row]):
            ret_val = int(val)
    return ret_val


def main(fi_name):
    grid = parse_file(fi_name)
    symbols = get_symbol_locations(grid)
    number_iterator = get_numbers(grid)
    numbers_total = 0
    for number in number_iterator:
        numbers_total += check_number(number, symbols)
    print(f"Total numbers: {numbers_total}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)