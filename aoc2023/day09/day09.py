import argparse
from aoc2023.utils import parse_file

def get_additive_numbers(number_list, end_numbers, start_numbers):
    if all([x == 0 for x in number_list]):
        total_end_numbers = sum(end_numbers)
        s = 0
        for i in range(len(start_numbers)-1, -1, -1):
            s = start_numbers[i] - s
        return total_end_numbers, s
    else:
        n_diffs = [number_list[i] - number_list[i-1] for i in range(1, len(number_list))]
        end_numbers.append(number_list[-1])
        start_numbers.append(number_list[0])
        return get_additive_numbers(n_diffs, end_numbers, start_numbers)

def main(fi_name):
    inputs = parse_file(fi_name)
    part1_numbers = []
    part2_numbers = []
    for row in inputs:
        p1, p2 = get_additive_numbers([int(x) for x in row.split(' ')], [], [])
        part1_numbers.append(p1)
        part2_numbers.append(p2)
    print(f"Part 1 total: {sum(part1_numbers)}")
    print(f"Part 2 totals: {sum(part2_numbers)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)