import re

puzzle = open('input10_2.txt').read()
from collections import defaultdict

def find_start(puzzle):
    lines = puzzle.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                return (x, y)

def is_bounded(pos, width, height):
    return 0 <= pos[0] < width and 0 <= pos[1] < height

def build_graph(puzzle):
    graph = defaultdict(lambda: [])
    lines = puzzle.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '-':
                graph[(x, y)].append((x - 1, y))
                graph[(x, y)].append((x + 1, y))
            elif char == '|':
                graph[(x, y)].append((x, y - 1))
                graph[(x, y)].append((x, y + 1))
            elif char == 'J':
                graph[(x, y)].append((x - 1, y))
                graph[(x, y)].append((x, y - 1))
            elif char == '7':
                graph[(x, y)].append((x - 1, y))
                graph[(x, y)].append((x, y + 1))
            elif char == 'L':
                graph[(x, y)].append((x + 1, y))
                graph[(x, y)].append((x, y - 1))
            elif char == 'F':
                graph[(x, y)].append((x + 1, y))
                graph[(x, y)].append((x, y + 1))
    start = find_start(puzzle)
    start_x, start_y = start
    for adjacent in [(start_x - 1, start_y), (start_x + 1, start_y), (start_x, start_y - 1), (start_x, start_y + 1)]:
        if start in graph[adjacent]:
            graph[start].append(adjacent)
    # trim out of bounds
    width = len(lines[0])
    height = len(lines)
    return {node: [adjacent for adjacent in graph[node] if is_bounded(adjacent, width, height)] for node in graph if graph[node]}

@profile
def max_cycle_depth(graph, start):
    stack = [(start, [])]
    max_visited = []
    while stack:
        curr, visited = stack.pop()
        if curr == start and visited:
            if len(visited) > len(max_visited):
                max_visited = visited
            continue
        if curr in visited:
            continue
        for adjacent in graph[curr]:
            stack.append((adjacent, visited + [curr]))
    return max_visited

# determine polarity of ray-intersecting given many pipes
def intersect_loop(loop_chars):
    result = False
    start = None
    for char in loop_chars:
        if char == 'F':
            assert start is None
            start = 'F'
        elif char == 'L':
            assert start is None
            start = 'L'
        elif char == '7':
            assert start == 'F' or start == 'L'
            if start == 'L':
                result = not result
            start = None
        elif char == 'J':
            assert start == 'F' or start == 'L'
            if start == 'F':
                result = not result
            start = None
        elif char == '|':
            assert start is None
            result = not result

    return result

# use ray-intersecting to count in loop
def count_enclosed(puzzle, loop):
    lines = puzzle.strip().split('\n')
    count = 0
    for y, line in enumerate(lines):
        enclosed = False
        loop_chars = []
        for x, char in enumerate(line):
            counted = False
            if (x, y) in loop:
                loop_chars.append(char)
            else:
                if intersect_loop(loop_chars):
                    enclosed = not enclosed
                loop_chars = []                
                if enclosed:
                    count += 1
                    counted = True
    return count

def negate_delta(x):
    return (-x[0], -x[1])

def find_start_char(cycle):
    start = cycle[0]
    first = cycle[1]
    last = cycle[-1]
    path_delta1 = (start[0] - last[0], start[1] - last[1])
    path_delta2 = (first[0] - start[0], first[1] - start[1])
    pipes = {
        '-': ((1, 0), (1, 0)),
        '|': ((0, 1), (0, 1)),
        'J': ((1, 0), (0, -1)),
        '7': ((1, 0), (0, 1)),
        'F': ((0, -1), (1, 0)),
        'L': ((0, 1), (1, 0))
    }
    for char, (pipe_delta1, pipe_delta2) in pipes.items():
        if (path_delta1, path_delta2) == (pipe_delta1, pipe_delta2):
            return char
        elif (path_delta1, path_delta2) == (negate_delta(pipe_delta2), negate_delta(pipe_delta1)):
            return char

    assert False

def solve(puzzle):
    start = find_start(puzzle)
    graph = build_graph(puzzle)
    cycle = max_cycle_depth(graph, start)
    solution1 = len(cycle) // 2
    start_char = find_start_char(cycle)
    solution2 = count_enclosed(puzzle.replace('S', start_char), cycle)
    return solution1, solution2

solution1, solution2 = solve(puzzle)
print('part1', solution1)
print('part2', solution2)
