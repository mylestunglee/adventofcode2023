import sys

def parse_grid_input(grid_input):
    return tuple(tuple(line) for line in grid_input.rstrip().split('\n'))

DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_DOWN = (0, -1)
DIRECTION_UP = (0, 1)

ADJACENTS  = {
    '.': [DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP],
    '>': [DIRECTION_RIGHT],
    'v': [DIRECTION_UP],
}

def add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))

def solve_part1(grid):
    width = len(grid[0])
    height = len(grid)
    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    [start] = [(x, 0) for x, char in enumerate(grid[0]) if char == '.']
    stack = [(start, [])]
    max_length = 0
    path = None

    while stack:
        curr, visited = stack.pop()
        if curr in visited:
            continue
        if not in_bounds(*curr):
            continue
        if grid[curr[1]][curr[0]] == '#':
            continue
        if curr[1] == height - 1:
            if len(visited) > max_length:
                print('new max_length', max_length)
                max_length = len(visited)
                path = visited
        for adj in ADJACENTS [grid[curr[1]][curr[0]]]:
            stack.append((add(curr, adj), visited + [curr]))
    
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if (x, y) in path:
                print('O', end='')
            else:
                print(char, end='')
        print()
    
    return len(path)

def solve_part2(grid):
    pass

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        grid_input = file.read()

    grid = parse_grid_input(grid_input)
    print('part1', solve_part1(grid))
    #print('part2', solve_part2(grid))
