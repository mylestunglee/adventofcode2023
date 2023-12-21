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
    'U': (0, -1),
    'D': (0, 1)
}

def simple_segments(puzzle):
    return [(direction, length) for direction, length, _ in puzzle]

def complex_segments(puzzle):
    return [('RDLU'[int(colour[5])], int(colour[:5], 16)) for _, _, colour in puzzle]

def simplify_segments(segments):
    result = []
    curr_length = 0
    curr_direction = None
    for direction, length in segments:
        if direction != curr_direction:
            if curr_length > 0:
                result.append((curr_direction, curr_length))
            curr_direction = direction
            curr_length = length
    if curr_length > 0:
        result.append((curr_direction, curr_length))

def is_clockwise(direction, next_direction):
    return (direction + next_direction) in ['RD', 'DL', 'LU', 'UR']

def find_vertices(segments):
    vertices = []
    x, y = (0.5, 0.5)
    for i, (direction, length) in enumerate(segments):
        next_direction, _ = segments[(i + 1) % len(segments)]
        dx, dy = OFFSETS[direction]
        ndx, ndy = OFFSETS[next_direction]
        x += length * dx
        y += length * dy
        if is_clockwise(direction, next_direction):
            vertices.append((round(x + 0.5*dx - 0.5*ndx), round(y + 0.5*dy - 0.5*ndy)))
        else:
            vertices.append((round(x - 0.5*dx + 0.5*ndx), round(y - 0.5*dy + 0.5*ndy)))

    return vertices

def polygon_area(vertices):
    double_area = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        double_area += x1*y2 - y1*x2
    return double_area // 2

def solve_part1(puzzle):
    segments = simple_segments(puzzle)
    vertices = find_vertices(segments)
    return polygon_area(vertices)

def solve_part2(puzzle):
    segments = complex_segments(puzzle)
    vertices = find_vertices(segments)
    return polygon_area(vertices)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(puzzle))
    print('part2', solve_part2(puzzle))
