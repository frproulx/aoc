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

def get_number_dict(grid):
    """For part 2"""
    numbers = defaultdict(list)
    for i, row in enumerate(grid):
        number_matches = re.finditer('[0-9]+', row)
        for number in number_matches:
            numbers[i].append((number.group(0), number.start()))
    return numbers

def get_gear_ratios(symbol_loc, number_dict):
    """ symbol_loc is (i,j) of symbol, number_dict is {i: (val, start_j)} of numbers"""
    candidate_numbers = []
    i, j = symbol_loc
    for i_delta in range(-1, 2):
        number_row = number_dict.get(i + i_delta, [])
        for number in number_row:
            if (j >= number[1] - 1) and (j <= number[1] + len(number[0])):
                candidate_numbers.append(int(number[0]))
    if len(candidate_numbers) == 2:
        return candidate_numbers[0] * candidate_numbers[1]
    else:
        return 0

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

    # Part 1 - all numbers
    number_iterator = get_numbers(grid)
    numbers_total = 0
    for number in number_iterator:
        numbers_total += check_number(number, symbols)
    print(f"Total numbers: {numbers_total}")

    # Part 2 - get gear ratios
    number_dict = get_number_dict(grid)

    total_gear_ratios = 0
    for symbol_i, symbol_j_list in symbols.items():
        for symbol_j in symbol_j_list:
            total_gear_ratios += get_gear_ratios((symbol_i, symbol_j), number_dict)
    print(f"Total gear ratios: {total_gear_ratios}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)