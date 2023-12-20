import sys
import re

def parse_line(line):
    direction, length_input, colour_input = line.split()
    return direction, int(length_input), colour_input[2:8]

def parse_puzzle_input(puzzle_input):
    return [parse_line(line) for line in puzzle_input.strip().split('\n')]

OFFSETS = {
    'L': (-1, 0),
    'R': (1, 0),
    'D': (0, -1),
    'U': (0, 1)
}

def add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))

def find_loop(puzzle):
    loop = set()
    curr = (0, 0)
    for direction, length, _ in puzzle:
        for _ in range(length):
            curr = add(curr, OFFSETS[direction])
            loop.add(curr)
    return loop

def solve_part1(puzzle):
    loop = find_loop(puzzle)
    xs, ys = zip(*loop)
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)
    visited = set()
    stack = [(x_min - 1, y_min - 1)]
    while stack:
        curr = stack.pop()
        if curr in loop:
            continue
        if curr[0] < x_min - 1 or curr[0] > x_max + 1 or curr[1] < y_min - 1 or curr[1] > y_max + 1:
            continue

        if curr in visited:
            continue
        visited.add(curr)
        
        for offset in OFFSETS.values():
            stack.append(add(curr, offset))
    return (3 + x_max - x_min) * (3 + y_max - y_min) - len(visited)

def solve_part2(puzzle):
    pass

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(puzzle))
    #print('part2', solve_part2(puzzle))
