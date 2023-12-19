import sys

def parse_grid_input(grid_input):
    return [list(line) for line in grid_input.split('\n')]

def parse_puzzle_input(puzzle_input):
    grid_inputs = puzzle_input.strip().split('\n\n')
    return [parse_grid_input(grid_input) for grid_input in grid_inputs]

with open(sys.argv[1]) as file:
    puzzle_input = file.read()

def count_differences(xs, ys):
    return sum(1 for x, y in zip(xs, ys) if x != y)

def horizontal_reflection_errors(grid, y):
    grid_height = len(grid)
    check_height = min(y, grid_height - y)
    return sum(count_differences(grid[y - j - 1], grid[y + j]) for j in range(check_height))

def find_horizontal_reflection(grid, errors):
    height = len(grid)
    reflections = []
    for y in range(1, height):
        if horizontal_reflection_errors(grid, y) == errors:
            reflections.append(y)
    return reflections

def transpose_grid(grid):
    return [list(cols) for cols in zip(*grid)]

def solve(grids, errors):
    total = 0
    for grid in grids:
        total += 100 * sum(find_horizontal_reflection(grid, errors))
        total += sum(find_horizontal_reflection(transpose_grid(grid), errors))
    return total

grids = parse_puzzle_input(puzzle_input)
print(solve(grids, 0))
print(solve(grids, 1))
