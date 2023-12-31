import sys
from collections import namedtuple
import numpy as np
import scipy
import random

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

def minimum_distance(proj1, proj2):
    a = proj2.position - proj1.position
    b = proj2.velocity - proj1.velocity
    if b.dot(b) == 0:
        return np.NAN
    mu = -(a.dot(b)) / b.dot(b)
    c = a + mu * b
    return c.dot(c)

def minimum_distances(proj1, projectiles):
    return sum(minimum_distance(proj1, proj2) for proj2 in projectiles)

def solve_velocity(projectiles, y0, w0):
    def cost(x):
        proj1 = Projectile(x[:3], x[3:])
        return minimum_distances(proj1, projectiles)

    x0 = np.concatenate((y0, w0))
    res = scipy.optimize.minimize(cost, x0, method='Nelder-Mead', tol=1e-12)
    print(res)
    return res.x[3:]

def solve_position(projectiles, y0, w):
    def cost(x):
        proj1 = Projectile(x, w)
        return minimum_distances(proj1, projectiles)

    res = scipy.optimize.minimize(cost, y0, method='Nelder-Mead', tol=1e-12)
    print(res)
    return res.x

def solve_part2(projectiles):
    proj = random.choice(projectiles)
    w = solve_velocity(projectiles, proj.position, proj.velocity)
    # assert w's are integers
    y = solve_position(projectiles, proj.position, w)
    # assert y's are integers
    return int(sum(y))

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    projectiles = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(projectiles))
    print('part2', solve_part2(projectiles))
