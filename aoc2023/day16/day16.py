import click
import sys
from aoc2023.utils import parse_file

sys.setrecursionlimit(50_000)

# delta_i (row), delta_j (col)

DIRECTION_MAP = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

TURN_MAPS = {
    '.': {d: d for d in 'NESW'},
    '\\': {
        'E': 'S',
        'N': 'W',
        'S': 'E',
        'W': 'N'
    },
    '/': {
        'E': 'N',
        'N': 'E',
        'S': 'W',
        'W': 'S'
    },
    '|': {
        'N': 'N',
        'S': 'S',
        'E': 'NS',
        'W': 'NS',
         },
    '-': {
        'W': 'W',
        'E': 'E',
        'N': 'EW',
        'S': 'EW'
    }
}


class Grid():
    def __init__(self, n_rows, n_cols):
        self.n_rows = int(n_rows)
        self.n_cols = int(n_cols)

        self.cell_map = {}
    
    def __repr__(self) -> str:
        rows = ['' for _ in range(self.n_rows)]
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                cell = self.cell_map[i * self.n_rows + j]
                if cell.energized and (cell.symbol == '.'):
                    rows[i] += '#'
                else:
                    rows[i] += cell.symbol
        return '\n'.join(rows)

    def add_cell(self, cell):
        self.cell_map[cell.i * self.n_rows + cell.j] = cell

    def get_cell(self, i, j):
        if (i < 0) or (i >= self.n_rows) or (j < 0) or (j >= self.n_cols):
            return None
        return self.cell_map[i * self.n_rows + j]
    
    def score(self, reset_state=True):
        total_score = sum([c.energized for c in self.cell_map.values()])
        if reset_state:
            for c in self.cell_map.values():
                c.energized = False
                c.directions_encountered = []
        return total_score
    
    def generate_edge_cells(self):
        total_cells = len(self.cell_map)

        for j in range(self.n_cols):
            yield j, 'S'  # top edge
            yield ((self.n_rows - 1) * (self.n_cols)) + j, 'N'  # bottom edge
        
        for i in range(total_cells // self.n_rows):
            yield i * self.n_cols, 'E'  # left edge
            yield (i * self.n_cols) + (self.n_cols - 1), 'W'  #right edge

class Cell():
    def __init__(self, i, j, symbol, grid):
        self.i = i
        self.j = j
        self.symbol = symbol
        self.energized = False
        self.grid = grid
        self.directions_encountered = []

    def __repr__(self) -> str:
        return f"{self.symbol} ({self.i}, {self.j}; directions encountered: {self.directions_encountered}"

    def get_cell(self, movement):
        new_i = self.i + movement[0]
        new_j = self.j + movement[1]
        return self.grid.get_cell(new_i, new_j)

    def energize(self, direction):
        # energize self
        if direction in self.directions_encountered:
            return None
        
        self.directions_encountered.append(direction)
        self.energized = True

        for d in TURN_MAPS[self.symbol][direction]:
            c = self.get_cell(DIRECTION_MAP[d])
            if c is not None:
                c.energize(d)
        return None

@click.command()
@click.argument('fi_name')
def main(fi_name):
    input = parse_file(fi_name)
    grid = Grid(n_rows = len(input), n_cols = len(input[0]))
    for i, row in enumerate(input):
        for j, symb in enumerate(row):
            grid.add_cell(Cell(i, j, symb, grid))
    grid.cell_map[0].energize('E')
    print(grid.score())

    optimum_start_scores = []
    for i, dir_ in grid.generate_edge_cells():
        grid.cell_map[i].energize(dir_)
        optimum_start_scores.append(grid.score())
    print(max(optimum_start_scores))

if __name__ == '__main__':
    main()