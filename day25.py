import sys
from collections import defaultdict, deque

def parse_puzzle_input(puzzle_input, ignore_edges):
    graph = defaultdict(lambda: [])
    edges = []
    for line in puzzle_input.rstrip().split('\n'):
        curr, _, adjs = line.partition(': ')
        for adj in adjs.split(' '):
            if {curr, adj} in ignore_edges:
                continue
            graph[curr].append(adj)
            graph[adj].append(curr)
    return dict(graph)

def traverse(start, graph):
    visited = set()
    paths = []
    stack = [start]
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        stack += graph[curr]
    return visited

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    # use graphviz to find edges
    graph = parse_puzzle_input(puzzle_input, [{'rfq', 'lsk'}, {'prk', 'gpz'}, {'zhg', 'qdv'}])
    for start in graph:
        visited = traverse(start, graph)
        break
    unvisited = set(graph.keys()) - visited
    solution = len(visited) * len(unvisited)
    print(solution)
