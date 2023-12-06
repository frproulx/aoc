import argparse
import re
from aoc2023.utils import parse_file

DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def find_first_number(line: str, include_spelled_out=False, invert=False):
    search_key = '[1-9]'
    if invert:
        line = line[::-1]
        digit_keys = [k[::-1] for k in DIGITS.keys()]
    else:
        digit_keys = DIGITS.keys()

    if include_spelled_out:
        digits_search = '|'.join([f'{digit}' for digit in digit_keys])
        search_key = f'([1-9]|{digits_search})'
    first_number = re.search(search_key, line)
    if not first_number:
        first_number = '0'
    else:
        first_number = first_number.group()
    if invert:
        first_number = first_number[::-1]
    return DIGITS.get(first_number, first_number)

def find_number(line: str, include_spelled_out=False):
    first_digit = find_first_number(line, include_spelled_out=include_spelled_out)
    last_digit = find_first_number(line, include_spelled_out=include_spelled_out, invert=True)
    
    return int(first_digit + last_digit)


def part1(input):
    numbers = [find_number(line) for line in input]
    print(f"Part 1 total numbers: {sum(numbers)}")

def part2(input):
    numbers = [find_number(line, include_spelled_out=True) for line in input]
    print(f"Part 2 total numbers: {sum(numbers)}")

def main(fi_name):
    input = parse_file(fi_name)
    part1(input)
    part2(input)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)