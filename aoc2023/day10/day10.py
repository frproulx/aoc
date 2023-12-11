import argparse

from aoc2023.utils import parse_file

def hash_position(i: int, j: int, n_cols: int):
    return (j * n_cols) + i

def dehash_position(position: int, n_cols: int):
    return position % n_cols, position // n_cols

# map of symbols to delta_i, delta_j for two directions
DIRECTIONS = {
    'S': (0, 1),
    'N': (0, -1),
    'E': (1, 0),
    'W': (-1, 0)
}
SYMBOL_MAP = {
    'S': ['N', 'E', 'S', 'W'],
    '|': ['N', 'S'],
    '-': ['E', 'W'],
    'L': ['N', 'E'],
    'J': ['N', 'W'],
    '7': ['S', 'W'],
    'F': ['S', 'E']
}

class Pipe():
    def __init__(self, i, j, symbol, n_rows, n_cols):
        self.neighbors = []
        self.i, self.j = i, j
        self.loc_id = hash_position(i, j, n_cols)
        self.symbol = symbol
        self.loop_id = None
        self.fully_connected = None
        exclude_dirs = []
        if i == 0:
            exclude_dirs.append('W')
        if i == n_cols:
            exclude_dirs.append('E')
        if j == 0:
            exclude_dirs.append('N')
        if j == n_rows:
            exclude_dirs.append('S')

        if symbol != '.':
            directions = [d for d in SYMBOL_MAP[symbol] if d not in exclude_dirs]
            for dir_ in directions:
                diff = DIRECTIONS[dir_]
                self.neighbors.append(hash_position(i + diff[0], j + diff[1], n_cols))

    def __repr__(self):
        return f"{self.loc_id}: {self.symbol} ({self.i}, {self.j}) with neighbors {self.neighbors}"
    
    def check_neighbor(self, neighbor_id, pipes):
        """Returns true if this pipe is in the identified neighbor's pipes"""
        if neighbor_id not in pipes.keys():
            return False
        return self.loc_id in pipes[neighbor_id].neighbors
    
    def check_fully_connected(self, pipes):
        self.fully_connected = all([self.check_neighbor(n, pipes) for n in self.neighbors])

    def get_next_neighbor(self, source_id):
        return [n for n in self.neighbors if n != source_id][0]
    
    def replace_start_position(self, n_cols):
        if not self.symbol == 'S':
            raise ValueError("This isn't the start!?")
        neighbor_positions = [dehash_position(xy, n_cols) for xy in self.neighbors]
        position_diffs = [(xy[0] - self.i, xy[1] - self.j) for xy in neighbor_positions]
        position_dirs = [dir_ for dir_, diffs in DIRECTIONS.items() if diffs in position_diffs]
        true_symbol = [symbol for symbol, dirs_ in SYMBOL_MAP.items() if set(dirs_) == set(position_dirs)]
        if len(true_symbol) != 1:
            raise ValueError("Fixing S didn't work!") 
        self.symbol = true_symbol[0]

def find_connected_pipes(start_id, test_neighbor, pipes):
    potential_loop = []
    prev_id = start_id
    pipe = pipes[start_id]
    next_neighbor = pipe.neighbors[test_neighbor]
    while pipe.check_neighbor(next_neighbor, pipes):
        pipe = pipes[next_neighbor]
        potential_loop.append(pipe.loc_id)
        next_neighbor = pipe.get_next_neighbor(prev_id)
        prev_id = pipe.loc_id

        if pipe.loc_id == start_id:
            return potential_loop, True
    return potential_loop, False
    
def calculate_interior_area(pipes, loop_ids, n_rows, n_cols):
    total_area = 0
    running_symbol = None
    for j in range(n_rows):
        inside = False
        for i in range(n_cols):
            pt_id = hash_position(i, j, n_cols)
            if pt_id in loop_ids:
                symbol = pipes[pt_id].symbol
                if symbol == '|':
                    inside = not inside
                elif symbol == '-':
                    continue
                elif not running_symbol:
                    running_symbol = symbol
                else:
                    directions = SYMBOL_MAP[symbol] + SYMBOL_MAP[running_symbol]
                    if ('N' in directions) and ('S' in directions):
                        inside = not inside
                    running_symbol = None
            else:
                if inside:
                    total_area += 1
    return total_area


def main(fi_name):
    inputs = parse_file(fi_name)
    n_rows = len(inputs)
    n_cols = len(inputs[0])
    print(f"{n_rows} rows, {n_cols} cols")
    all_pipes = {}
    for j, row in enumerate(inputs):
        for i, c in enumerate(row):
            pipe = Pipe(i, j, c, n_rows, n_cols)
            all_pipes[pipe.loc_id] = pipe
    for p in all_pipes.values():
        p.check_fully_connected(all_pipes)
    # Delete bad pipes
    all_pipes = {id_: pipe for id_, pipe in all_pipes.items() 
                 if ((len(pipe.neighbors) == 2) and pipe.fully_connected) or (pipe.symbol == 'S')}

    start_id = [k for k, v in all_pipes.items() if v.symbol == 'S'][0]
    start_pipe = all_pipes[start_id]
    for n in start_pipe.neighbors:
        if n not in all_pipes.keys():
            start_pipe.neighbors = [q for q in start_pipe.neighbors if q != n]
        elif not start_pipe.check_neighbor(n, all_pipes):
            start_pipe.neighbors = [q for q in start_pipe.neighbors if q != n]
    valid_loop = False
    test_neighbor = 0
    while not valid_loop:
        loop_ids, valid_loop = find_connected_pipes(start_id, test_neighbor, all_pipes)
        test_neighbor += 1
    
    print(f"The farthest position is at {len(loop_ids) / 2}")
    start_pipe.replace_start_position(n_cols=n_cols)
    total_area = calculate_interior_area(all_pipes, loop_ids, n_rows, n_cols)
    print(f"Total interior area: {total_area}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)