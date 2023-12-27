import sys
from collections import defaultdict

def parse_values(value_inputs):
    return list(int(value) for value in value_inputs.split(','))

def parse_line(line, i):
    pos1_input, _, pos2_input = line.partition('~')
    pos1 = parse_values(pos1_input)
    pos2 = parse_values(pos2_input)
    assert all(u <= v for u, v in zip(pos1, pos2))
    assert sum(1 for u, v in zip(pos1, pos2) if u == v) >= 2
    return pos1, pos2, i

def parse_puzzle_input(puzzle_input):
    cubes = [parse_line(line, i) for i, line in enumerate(puzzle_input.rstrip().split('\n'))]
    cubes.sort(key=lambda cube: cube[0][-1])
    return cubes

def range_intersects(a_min, a_max, b_min, b_max):
    return a_min <= b_max and b_min <= a_max

def cube_intersects(cube1, cube2):
    return range_intersects(cube1[0][2], cube1[1][2], cube2[0][2], cube2[1][2]) \
        and range_intersects(cube1[0][0], cube1[1][0], cube2[0][0], cube2[1][0]) \
        and range_intersects(cube1[0][1], cube1[1][1], cube2[0][1], cube2[1][1])

def cubes_below(cube, cubes):
    z_below = cube[0][2] - 1
    z_cross_section = ((cube[0][0], cube[0][1], z_below), (cube[1][0], cube[1][1], z_below), cube[2])
    return [other[2] for other in cubes if cube_intersects(z_cross_section, other)]

def settle_cubes(cubes):
    graph = {}
    for i in range(len(cubes)):
        while cubes[i][0][2] >= 2:
            others = cubes_below(cubes[i], cubes)
            if others:
                graph[cubes[i][2]] = others
                break
            
            cubes[i][0][2] -= 1
            cubes[i][1][2] -= 1
        else:
            graph[cubes[i][2]] = []
    return graph

def solve_part1(graph):
    return sum(1 for node in graph if all([node] != nexts for nexts in graph.values()))

def reverse_graph(graph):
    result = defaultdict(lambda: [])
    for curr, adjs in graph.items():
        for adj in adjs:
            result[adj].append(curr)
    return result

def count_fall(node, graph, reversed_graph):
    fallen = {node}
    stack = reversed_graph[node][:]
    while stack:
        curr = stack.pop()
    
        if not all(adj in fallen for adj in graph[curr]):
            continue

        fallen.add(curr)
        stack += reversed_graph[curr]
    # Exclude node in fallen
    return len(fallen) - 1

def solve_part2(graph):
    reversed_graph = reverse_graph(graph)
    return sum(count_fall(node, graph, reversed_graph) for node in graph)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    cubes = parse_puzzle_input(puzzle_input)
    graph = settle_cubes(cubes)
    print('part1', solve_part1(graph))
    print('part2', solve_part2(graph))
