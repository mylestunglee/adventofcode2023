import sys
from collections import deque

def parse_puzzle_input(puzzle_input):
    grid = tuple(tuple(line) for line in puzzle_input.strip().replace('S', '.').split('\n'))
    [start] = [(x, y) for y, line in enumerate(puzzle_input.strip().split('\n')) for x, char in enumerate(line) if char == 'S']
    return start, grid

def adjacents(pos):
    x, y = pos
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)

def solve_part1(start, grid, length=64):
    width = len(grid[0])
    height = len(grid)
    def in_bounds(pos):
        return 0 <= pos[0] < width and 0 <= pos[1] < height

    visited = {}
    stack = deque()
    stack.append((start, length))
    while stack:
        curr, remaining = stack.popleft()
        if curr in visited:
            continue
        if not in_bounds(curr):
            continue
        if grid[curr[1]][curr[0]] != '.':
            continue
        visited[curr] = remaining
        if remaining == 0:
            continue
        for adjacent in adjacents(curr):
            stack.append((adjacent, remaining - 1))
    return sum(1 for count in visited.values() if (count % 2 == 0) == (length % 2 == 0))

def solve_part2(start, grid):
    n = 26501365
    a = len(grid)
    a1 = len(grid[0])
    assert(a == a1)
    b, b1 = start
    assert b == b1
    assert b * 2 + 1 == a
    center = solve_part1(start, grid, 2 * b)
    c = (n - (b + 1)) % a
    assert c + 1 == a
    corners = [solve_part1(substart, grid, c) for substart in [(c, b + 1), (0, b + 1), (b + 1, 0), (b + 1, c)]]
    print(c - (b + 1))

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    # print('part1', solve_part1(*puzzle))
    print('part2', solve_part2(*puzzle))

