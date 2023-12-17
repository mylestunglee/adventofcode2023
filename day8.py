import re
import math
puzzle_input = open('input08_2.txt').read()

def parse_puzzle_input(puzzle_input):
    instructions_input, graph_input = puzzle_input.strip().split('\n\n')
    instructions = [{'L': 0, 'R': 1}[instruction] for instruction in instructions_input]
    graph = {}
    for line in graph_input.split('\n'):
        matches = re.match('([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)', line)
        node, left, right = matches.groups()
        graph[node] = (left, right)
    return instructions, graph

def solve1(instructions, graph):
    curr = 'AAA'
    visited = set()
    turn = 0
    while True:
        instruction_index = turn % len(instructions)	
        
        if (curr, instruction_index) in visited:
            print('cycle detected')
            return None
        
        visited.add((curr, instruction_index))
        
        if curr == 'ZZZ':
            return turn
    
        instruction = instructions[instruction_index]
        curr = graph[curr][instruction]
        turn += 1

def find_cyclic_path(instructions, graph, start):
    curr = start
    visited = set()
    turn = 0
    path = []
    while True:
        instruction_index = turn % len(instructions)	
        
        if (curr, instruction_index) in visited:
            return path[:instruction_index], path[instruction_index:]
        
        visited.add((curr, instruction_index))
        path.append(curr)
        
        instruction = instructions[instruction_index]
        curr = graph[curr][instruction]
        turn += 1

def find_finish_cyclic_depth(instructions, graph, start, finish_predicate):
    noncyclic_path, cyclic_path = find_cyclic_path(instructions, graph, start)
    noncyclic_depths = [i for i, node in enumerate(noncyclic_path) if finish_predicate(node)]
    cyclic_start = len(noncyclic_path)
    cyclic_length = len(cyclic_path)
    cyclic_depths = [i for i, node in enumerate(cyclic_path) if finish_predicate(node)]
    return noncyclic_depths, cyclic_start, cyclic_length, cyclic_depths

def solve2(instructions, graph):
    lengths = []
    for node in graph:
        if node[-1] == 'A':
            noncyclic_depths, cyclic_start, cyclic_length, cyclic_depths = find_finish_cyclic_depth(instructions, graph, node, lambda node: node[-1] == 'Z')
            assert not noncyclic_depths
            assert len(cyclic_depths) == 1
            assert cyclic_depths[0] + cyclic_start == cyclic_length
            lengths.append(cyclic_length)
    return math.lcm(*lengths)    

instructions, graph = parse_puzzle_input(puzzle_input)
print('part1', solve1(instructions, graph))
print('part2', solve2(instructions, graph))
