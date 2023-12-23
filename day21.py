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

def solve_part1(start, grid, length=64, parity=True):
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
    # return sum(1 for count in visited.values() if (count % 2 == 0) == (length % 2 == 0))
    return sum(1 for count in visited.values() if (count % 2 == 0) == parity)



def solve_part2(start, grid):
    # Assumes the:
    # 1. Grid edges are all dots,
    # 2. S is on a row of dots
    # 3. S is on a column of dots
    # 4. end > mid + 1, otherwise the diag tile counts will differ
    inital_steps = 26501365
    grid_size = len(grid)
    grid_width = len(grid[0])
    assert(grid_size == grid_width)
    mid, mid_y = start
    assert mid == mid_y
    assert mid * 2 + 1 == grid_size
    end = (inital_steps - (mid + 1)) % grid_size
    assert end + 1 == grid_size
    
    corner_fills = [solve_part1(substart, grid, end, True) for substart in [(end, mid), (0, mid), (mid, 0), (mid, end)]]
    
    short_diag_steps = end - (mid + 1)
    short_diag_fills = [solve_part1(substart, grid, short_diag_steps, True) for substart in [(0, 0), (0, end), (end, 0), (end, end)]]
    
    long_diag_steps = short_diag_steps + grid_size
    long_diag_fills = [solve_part1(substart, grid, long_diag_steps, True) for substart in [(0, 0), (0, end), (end, 0), (end, end)]]
    
    tile_radius = (inital_steps - mid) // grid_size
    
    outer_ring_count = (tile_radius - 2) // 2
    inner_ring_count = (tile_radius - 2) - outer_ring_count
    inner_ring_fill = solve_part1(start, grid, 2 * mid, inital_steps % 2 == 0)
    outer_ring_fill = solve_part1(start, grid, 2 * mid, inital_steps % 2 != 0)
    inner_ring_tiles = 1 + 4*inner_ring_count*(inner_ring_count + 1)
    outer_ring_tiles = 4*(outer_ring_count + 1)*(outer_ring_count + 1)
    
    return sum(corner_fills) + tile_radius*sum(short_diag_fills) + (tile_radius - 1)*sum(long_diag_fills) + inner_ring_tiles*inner_ring_fill + outer_ring_tiles*outer_ring_fill

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(*puzzle))
    print('part2', solve_part2(*puzzle))
