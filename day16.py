import sys
from collections import defaultdict

def parse_puzzle_input(puzzle_input):
    return tuple(tuple(line) for line in puzzle_input.strip().split('\n'))

DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_DOWN = (0, -1)
DIRECTION_UP = (0, 1)

MIRRORS = {
    '.': {
        DIRECTION_LEFT: [DIRECTION_LEFT],
        DIRECTION_RIGHT: [DIRECTION_RIGHT],
        DIRECTION_DOWN: [DIRECTION_DOWN],
        DIRECTION_UP: [DIRECTION_UP]
    },
    '/': {
        DIRECTION_LEFT: [DIRECTION_UP],
        DIRECTION_RIGHT: [DIRECTION_DOWN],
        DIRECTION_DOWN: [DIRECTION_RIGHT],
        DIRECTION_UP: [DIRECTION_LEFT]
    },
    '\\': {
        DIRECTION_LEFT: [DIRECTION_DOWN],
        DIRECTION_RIGHT: [DIRECTION_UP],
        DIRECTION_DOWN: [DIRECTION_LEFT],
        DIRECTION_UP: [DIRECTION_RIGHT]
    },
    '-': {
        DIRECTION_LEFT: [DIRECTION_LEFT],
        DIRECTION_RIGHT: [DIRECTION_RIGHT],
        DIRECTION_DOWN: [DIRECTION_LEFT, DIRECTION_RIGHT],
        DIRECTION_UP: [DIRECTION_LEFT, DIRECTION_RIGHT]
    },
    '|': {
        DIRECTION_LEFT: [DIRECTION_DOWN, DIRECTION_UP],
        DIRECTION_RIGHT: [DIRECTION_DOWN, DIRECTION_UP],
        DIRECTION_DOWN: [DIRECTION_DOWN],
        DIRECTION_UP: [DIRECTION_UP]
    }
}

def in_bounds(curr, grid):
    width = len(grid[0])
    height = len(grid)
    return 0 <= curr[0] < width and 0 <= curr[1] < height

def add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))

def count_energized(grid, start, direction):
    visited = set()
    stack = [(start, direction)]
    while stack:
        curr, direction = stack.pop()

        if not in_bounds(curr, grid):
            continue

        if (curr, direction) in visited:
            continue

        visited.add((curr, direction))

        cell = grid[curr[1]][curr[0]]
        new_directions = MIRRORS[cell][direction]
        for new_direction in new_directions:
            stack.append((add(curr, new_direction), new_direction))
    return len({curr for curr, _ in visited})

def solve_part1(grid):
    return count_energized(grid, (0, 0), DIRECTION_RIGHT)

def edges(grid):
    width = len(grid[0])
    height = len(grid)
    for x in range(width):
        yield (x, 0), DIRECTION_UP
        yield (x, height - 1), DIRECTION_DOWN
    for y in range(height):
        yield (0, y), DIRECTION_RIGHT
        yield (width - 1, y), DIRECTION_LEFT

def solve_part2(grid):
    return max(count_energized(grid, start, direction) for start, direction in edges(grid))

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(puzzle))
    print('part2', solve_part2(puzzle))
