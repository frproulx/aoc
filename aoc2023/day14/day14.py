import click
import hashlib
from aoc2023.utils import parse_file

class Platform():
    def __init__(self, inputs):
        self.positions = inputs
        self.orientation = 0
    
    def __repr__(self):
        return '\n'.join(self.positions)
    
    def rotate_clockwise(self):
        new_positions = ['' for _ in self.positions[0]]
        for j in self.positions:
            for i, v in enumerate(j):
                new_positions[i] = v + new_positions[i]
        
        self.positions = new_positions
        if self.orientation < 3:
            self.orientation += 1
        else:
            self.orientation = 0
    
    def shift_rocks(self):
        new_positions = []
        for row in self.positions:
            new_row = []
            for group in row.split('#'):
                new_row.append(''.join(sorted(group)))
            new_positions.append('#'.join(new_row))

        self.positions = new_positions

    def score(self):
        for _ in range(4):
            if self.orientation == 0:
                rev_positions = reversed(self.positions.copy())
                total_score = 0
                for i, row in enumerate(rev_positions):
                    total_score += sum([x == 'O' for x in row]) * (i + 1)
            self.rotate_clockwise()
        return total_score
    
    def step(self):
        self.rotate_clockwise()
        self.shift_rocks()
        score = self.score()
        return {
            'full_positions': ''.join(self.positions).encode(),
            'score': score}


def make_hash_key(hash_map, payload):
    m = hashlib.md5()
    m.update(payload['full_positions'])
    if m.hexdigest() not in hash_map.keys():
        return m.hexdigest()
    while m.hexdigest() in hash_map.keys():
        if hash_map[m.hexdigest()]['full_positions'] != payload['full_positions']:
            m.update(payload['full_positions'])
        else:
            return None
    return m.hexdigest()


@click.command()
@click.argument('fi_name')
def main(fi_name):
    inputs = parse_file(fi_name)
    platform = Platform(inputs)

    platform_positions = {}

    for iter_ in range(1_000_000_000 - 1):
        payload = platform.step()
        m = make_hash_key(platform_positions, payload)
        payload['rotation'] = iter_
        if not m:
            break
        platform_positions[m] = payload

    n_entries = len(platform_positions)
    restart_position = [v['rotation'] for k, v in platform_positions.items() if v['full_positions'] == payload['full_positions']][0]
    
    initial_key = [k for k, v in platform_positions.items() if v['rotation'] == 0][0]

    final_position = restart_position + ((4 * (1_000_000_000 - restart_position)) % (4 * (n_entries - restart_position)))
    final_key = [k for k,v in platform_positions.items() if v['rotation'] == final_position][0]

    print(
        """Total scores-\n"""
        f"""\tpart 1: {platform_positions[initial_key]['score']}\n"""
        f"""\tpart 2: {platform_positions[final_key]['score']}"""
    )

if __name__ == '__main__':
    main()