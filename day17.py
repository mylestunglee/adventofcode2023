import sys
import heapq

def parse_puzzle_input(puzzle_input):
    return tuple(tuple(int(char) for char in line) for line in puzzle_input.strip().split('\n'))

DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_DOWN = (0, -1)
DIRECTION_UP = (0, 1)
DIRECTIONS = [DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP]
DIRECTION_NONE = (0, 0)

def add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))

def negate(xs):
    return tuple(-x for x in xs)

def in_bounds(curr, grid):
    width = len(grid[0])
    height = len(grid)
    return 0 <= curr[0] < width and 0 <= curr[1] < height

def traverse(grid, min_straight, max_straight):
    width = len(grid[0])
    height = len(grid)
    def f(heat_loss, pos):
        return heat_loss + (width - pos[0] - 1 + height - pos[1] - 1)

    least_heat_loss = {}
    queue = []
    visited = set()
    heapq.heappush(queue, (0, 0, (0, 0), tuple([DIRECTION_NONE] * max_straight)))
    target = (len(grid[0]) - 1, len(grid) - 1)
    while queue:
        _, heat_loss, curr_pos, prev_dirs = heapq.heappop(queue)
        
        if curr_pos == target:
            return heat_loss

        if heat_loss < least_heat_loss.get((curr_pos, prev_dirs), sys.maxsize):
            least_heat_loss[(curr_pos, prev_dirs)] = heat_loss
        else:
            continue

        for curr_dir in DIRECTIONS:
            # If not travelling in the same direction for at least min_straight blocks
            if min_straight > 0 and len(set(prev_dirs[:min_straight])) != 1 and curr_dir != prev_dirs[0]:
                continue
            # If travelling in the same direction for max_straight blocks:
            if len(set(list(prev_dirs) + [curr_dir])) == 1:
                continue
            if curr_dir == negate(prev_dirs[0]):
                continue # cannot go back
            next_pos = add(curr_pos, curr_dir)
            if not in_bounds(next_pos, grid):
                continue

            next_heat_loss = heat_loss + grid[next_pos[1]][next_pos[0]]
            next_prev_dirs = tuple([curr_dir] + list(prev_dirs)[:max_straight - 1])
            heapq.heappush(queue, (f(next_heat_loss, next_pos), next_heat_loss, next_pos, next_prev_dirs))

def solve_part1(grid):
    return traverse(grid, 0, 3)

def solve_part2(grid):
    return traverse(grid, 4, 10)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(puzzle))
    print('part2', solve_part2(puzzle))
