import sys
from collections import defaultdict

def parse_grid_input(grid_input):
    return tuple(tuple(line) for line in grid_input.rstrip().split('\n'))

DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_DOWN = (0, -1)
DIRECTION_UP = (0, 1)
DIRECTIONS = [DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP]

ADJACENTS  = {
    '.': DIRECTIONS,
    '>': [DIRECTION_RIGHT],
    'v': [DIRECTION_UP],
}

def add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))

def negate(xs):
    return tuple(-x for x in xs)

def solve_part1(grid):
    width = len(grid[0])
    height = len(grid)
    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    [start] = [(x, 0) for x, char in enumerate(grid[0]) if char == '.']
    stack = [(start, [])]
    
    while stack:
        curr, visited = stack.pop()
        if curr in visited:
            continue
        if not in_bounds(*curr):
            continue
        if grid[curr[1]][curr[0]] == '#':
            continue
        if curr[1] == height - 1:
            return len(visited)
        for adj in ADJACENTS [grid[curr[1]][curr[0]]]:
            stack.append((add(curr, adj), visited + [curr]))

def get_directions(curr, prev_dir, grid):
    width = len(grid[0])
    height = len(grid)
    def in_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    directions = []
    for direction in DIRECTIONS:
        neighbour = add(curr, direction)
        if not in_bounds(*neighbour):
            continue
        if grid[neighbour[1]][neighbour[0]] == '#':
            continue
        if direction == negate(prev_dir):
            continue
        directions.append(direction)
    return directions

def trace_graph(grid):
    [start] = [(x, 0) for x, char in enumerate(grid[0]) if char == '.']
    [finish] = [(x, len(grid) - 1) for x, char in enumerate(grid[-1]) if char == '.']
    stack = [(start, start, DIRECTION_UP, 0)]
    graph = defaultdict(lambda: [])
    visited = set()
    
    def add_edge(source, target, weight):
        graph[source].append((weight, target))
        graph[target].append((weight, source))
    
    while stack:
        prev_node, curr, prev_dir, length = stack.pop()

        if curr in graph:
            add_edge(prev_node, curr, length)
            continue
        if curr in visited:
            continue
        visited.add(curr)

        if curr == finish:
            add_edge(prev_node, finish, length)
            continue

        directions = get_directions(curr, prev_dir, grid)
        
        if len(directions) == 1:
            stack.append((prev_node, add(curr, directions[0]), directions[0], length + 1))
        else:
            add_edge(prev_node, curr, length)
            for direction in directions:
                stack.append((curr, add(curr, direction), direction, 1))
    
    return start, finish, graph

def longest_path(start, finish, graph):
    lengths = []
    stack = [(start, 0, set())]
    while stack:
        curr, length, visited = stack.pop()
        if curr == finish:
            lengths.append(length)
            continue
        if curr in visited:
            continue
        for weight, neighbour in graph[curr]:
            stack.append((neighbour, length + weight, visited | {curr}))

    return max(lengths)

def solve_part2(grid):
    start, finish, graph = trace_graph(grid)
    return longest_path(start, finish, graph)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        grid_input = file.read()

    grid = parse_grid_input(grid_input)
    print('part1', solve_part1(grid))
    print('part2', solve_part2(grid))
