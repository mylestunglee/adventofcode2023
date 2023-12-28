import sys
from collections import namedtuple
import numpy as np

Projectile = namedtuple('Projectile', ['position', 'velocity'])

def parse_array(line):
    return np.array([float(token) for token in line.split(', ')])

def parse_projectile(line):
    position_input, _, velocity_input = line.partition(' @ ')
    return Projectile(parse_array(position_input), parse_array(velocity_input))

def parse_puzzle_input(puzzle_input):
    return [parse_projectile(line) for line in puzzle_input.rstrip().split('\n')]

def intersect(proj1, proj2):
    min_pos = 200000000000000
    max_pos = 400000000000000
    x1 = proj1.position[0]
    x2 = proj1.position[0] + proj1.velocity[0]
    x3 = proj2.position[0]
    x4 = proj2.position[0] + proj2.velocity[0]
    y1 = proj1.position[1]
    y2 = proj1.position[1] + proj1.velocity[1]
    y3 = proj2.position[1]
    y4 = proj2.position[1] + proj2.velocity[1]
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return False
    numer1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    numer2 = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)
    t = numer1 / denom
    u = numer2 / denom
    z = proj1.position + t * proj1.velocity
    return t >= 0 and u >= 0 and min_pos <= z[0] <= max_pos and min_pos <= z[1] <= max_pos

def solve_part1(projectiles):
    return sum(1 for i1, proj1 in enumerate(projectiles) for i2, proj2 in enumerate(projectiles) if i1 < i2 and intersect(proj1, proj2))

def solve_part2(projectiles):
    pass

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    projectiles = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(projectiles))
    #print('part2', solve_part2(projectiles))
