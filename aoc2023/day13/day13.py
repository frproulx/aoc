import click
from aoc2023.utils import parse_file

def check_breakpoint(fwd_list, rev_list, breakpoint, nrows, n_unequal):
    if breakpoint < nrows / 2:
        range_length = breakpoint
    else:
        range_length = nrows - breakpoint
    
    start_index = max(breakpoint - range_length, 0)
    end_index = breakpoint
    fwd_slice = ''.join(fwd_list[start_index:end_index])
    rev_slice = ''.join(rev_list[nrows - end_index - range_length: nrows - start_index - range_length])
    return sum([x != y for x,y in zip(fwd_slice, rev_slice)]) == n_unequal
    
def score_grid(grid, n_unequal):
    nrows = len(grid)

    grid_rev = grid.copy()
    grid_rev.reverse()

    for i in range(1, nrows):
        if check_breakpoint(grid, grid_rev, i, nrows, n_unequal):
            return i
    return None
        
def invert_grid(grid):
    output_grid = ['' for _ in grid[0]]
    for row in grid:
        for j, val in enumerate(row):
            output_grid[j] += val
    return output_grid

def score_input(input, n_unequal):
    row_score = score_grid(input, n_unequal)
    if row_score:
        return ('row', row_score)
    input = invert_grid(input)
    col_score = score_grid(input, n_unequal)
    return ('col', col_score)

@click.command()
@click.argument('fi_name')
def main(fi_name):
    inputs = parse_file(fi_name)
    grid = []
    all_scores_1 = []
    all_scores_2 = []
    for row in inputs:
        if row == '':
            all_scores_1.append(
                score_input(grid, n_unequal=0)
            )
            all_scores_2.append(
                score_input(grid, n_unequal=1)
            )
            grid = []
        else:
            grid.append(row)
    all_scores_1.append(score_input(grid, n_unequal=0))
    all_scores_2.append(
                score_input(grid, n_unequal=1)
            )
    total_score_1 = sum([c[1] for c in all_scores_1 if c[0] == 'row']) * 100 \
            + sum([c[1] for c in all_scores_1 if c[0] == 'col'])
    total_score_2 = sum([c[1] for c in all_scores_2 if c[0] == 'row']) * 100 \
            + sum([c[1] for c in all_scores_2 if c[0] == 'col'])
    print(f"Total scores: 1 - {total_score_1}; 2 - {total_score_2}")

if __name__ == '__main__':
    main()