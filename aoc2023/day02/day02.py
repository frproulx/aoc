import argparse
from aoc2023.utils import parse_file

CONSTRAINT = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def parse_round(round_str: str):
    ball_counts = round_str.split(',')
    ball_count_dict = {bc.strip().split(' ')[1]: int(bc.strip().split(' ')[0]) for bc in ball_counts}
    return ball_count_dict

def validate_round(round, constraint=CONSTRAINT):
    for color, count in round.items():
        if count > constraint[color]:
            return False
    return True

def max_cubes(rounds):
    max_counts = {'red': 0, 'green': 0, 'blue': 0}
    for round in rounds:
        for color, count in round.items():
            max_counts[color] = max(max_counts[color], count)
    return max_counts

def power(cube_count):
    pow_ = 1
    for ct in cube_count.values():
        pow_ *= ct
    return pow_

def main(fi_name):
    input = parse_file(fi_name)
    id_total = 0
    power_total = 0
    for game in input:
        game_id, rounds = game.split(':')
        game_number = game_id.strip('Game ')
        rounds_list = [parse_round(round) for round in rounds.split(';')]
        if all([validate_round(round) for round in rounds_list]):
            id_total += int(game_number)
        
        power_total += power(max_cubes(rounds_list))

    print(f"Total of IDs for valid games: {id_total}")
    print(f"The total power is {power_total}")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)