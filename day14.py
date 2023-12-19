import sys

def parse_puzzle_input(puzzle_input):
    return tuple(tuple(line) for line in puzzle_input.strip().split('\n'))

def calc_cube_positions(grid):
    return {(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == '#'}

def count_round(grid, sx, sy, dx, dy):
    width = len(grid[0])
    height = len(grid)
    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height
    count = 0
    x = sx
    y = sy
    while in_bounds(x, y) and grid[y][x] != '#':
        if grid[y][x] == 'O':
            count += 1
        x += dx
        y += dy
    return count    

def next_round_positions(grid, cube_positions, dx, dy, side):
    round_positions = set()

    for cube_position in cube_positions | side:
        sx = cube_position[0] + dx
        sy = cube_position[1] + dy
        count = count_round(grid, sx, sy, dx, dy)
        for i in range(count):
            round_positions.add((sx + i*dx, sy + i*dy))
    
    return round_positions

def next_grid(grid, cube_positions, round_positions):
    width = len(grid[0])
    height = len(grid)

    def cell(x, y):
        if (x, y) in cube_positions:
            return '#'
        elif (x, y) in round_positions:
            return 'O'
        else:
            return '.'

    return tuple(tuple(cell(x, y) for x in range(width)) for y in range(height))

def slide_round(grid, cube_positions, dx, dy, side):
    round_positions = next_round_positions(grid, cube_positions, -dx, -dy, side)
    return next_grid(grid, cube_positions, round_positions)

def slide_north(grid, cube_positions):
    width = len(grid[0])
    return slide_round(grid, cube_positions, 0, -1, {(x, -1) for x in range(width)})

def slide_west(grid, cube_positions):
    height = len(grid)
    return slide_round(grid, cube_positions, -1, 0, {(-1, y) for y in range(height)})

def slide_south(grid, cube_positions):
    width = len(grid[0])
    height = len(grid)
    return slide_round(grid, cube_positions, 0, 1, {(x, height) for x in range(width)})

def slide_east(grid, cube_positions):
    width = len(grid[0])
    height = len(grid)
    return slide_round(grid, cube_positions, 1, 0, {(width, y) for y in range(height)})

def slide_cycle(grid, cube_positions):
    grid = slide_north(grid, cube_positions)
    grid = slide_west(grid, cube_positions)
    grid = slide_south(grid, cube_positions)
    grid = slide_east(grid, cube_positions)
    return grid

def weigh(grid):
    height = len(grid)
    return sum((height - y) * sum(1 for cell in row if cell == 'O') for y, row in enumerate(grid))

def print_grid(grid):
    for line in grid:
        print(''.join(line))

def solve1(grid):
    cube_positions = calc_cube_positions(grid)
    grid2 = slide_north(grid, cube_positions)
    return weigh(grid2)

def solve2(grid):
    cube_positions = calc_cube_positions(grid)
    visited_set = {}
    visited_path = []
    cycle_start = None
    cycle_length = None
    steps = 0
    while not grid in visited_set:
        visited_set[grid] = steps
        visited_path.append(grid)
        grid = slide_cycle(grid, cube_positions)
        steps += 1
    cycle_start = visited_set[grid]
    cycle_length = steps - cycle_start
    target_index = 1000000000
    path_index = (target_index - cycle_start) % cycle_length + cycle_start
    target_grid = visited_path[path_index]
    return weigh(target_grid)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve1(puzzle))
    print('part2', solve2(puzzle))
