import sys

def transpose_grid(grid):
    return [list(cols) for cols in zip(*grid)]

def split_col(weight, col):
    chars = []
    for j, char in enumerate(col):
        if char == '#':
            if chars:
                yield weight - j + len(chars), ''.join(chars)
                chars = []
        else:
            chars.append(char)
    if chars:
        yield weight - len(col) + len(chars), ''.join(chars)

def parse_puzzle_input(puzzle_input):
    grid = puzzle_input.strip().split('\n')
    height = len(grid[0])
    cols = [(height, ''.join(col)) for col in transpose_grid(grid)]
    segments = [(weight, segment) for first_weight, col in cols for weight, segment in split_col(first_weight, col)]
    return segments

def triangle_number(x):
    return (x * (x + 1)) // 2

def solve_segment(weight, segment):
    rocks = sum(1 for char in segment if char == 'O')
    x = triangle_number(weight) - triangle_number(weight - rocks)
    #print(weight, segment, x)
    return x

def solve(segments):
    return sum(solve_segment(weight, segment) for weight, segment in segments)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print(solve(puzzle))
