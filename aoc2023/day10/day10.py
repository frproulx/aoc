import argparse

from aoc2023.utils import parse_file

def hash_position(i: int, j: int, n_rows: int):
    return j * n_rows + i

def dehash_position(position: int, n_rows: int):
    return position % n_rows, position // n_rows

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
        self.loc_id = hash_position(i, j, n_rows)
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
                self.neighbors.append(hash_position(i + diff[0], j + diff[1], n_rows))

    def __repr__(self):
        return f"{self.symbol} ({self.i}, {self.j}) with neighbors {self.neighbors}"
    
    def check_neighbor(self, neighbor_id, pipes):
        """Returns true if this pipe is in the identified neighbor's pipes"""
        if neighbor_id not in pipes.keys():
            return False
        return self.loc_id in pipes[neighbor_id].neighbors
    
    def check_fully_connected(self, pipes):
        self.fully_connected = all([self.check_neighbor(n, pipes) for n in self.neighbors])

    def get_next_neighbor(self, source_id):
        return [n for n in self.neighbors if n != source_id][0]
    

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
    

def main(fi_name):
    inputs = parse_file(fi_name)
    n_rows = len(inputs)
    n_cols = len(inputs[0])
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)