import sys
from collections import defaultdict

def parse_puzzle_input(puzzle_input):
    return list(puzzle_input.strip().split(','))

def hash(chars):
    curr = 0
    for char in chars:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr

def solve1(puzzle):
    return sum(hash(step) for step in puzzle)

def focusing_power(box):
    return sum((lens_i + 1) * focal_length for lens_i, (_, focal_length) in enumerate(box.items()))

def solve2(puzzle):
    boxes = defaultdict(lambda: {})
    for step in puzzle:
        if '-' in step:
            label = step[:-1]
            operation = '-'
        elif '=' in step:
            label, index_input = step.split('=')
            focal_length = int(index_input)
            operation = '='
        index = hash(label)

        if operation == '-':
            if label in boxes[index]:
                del boxes[index][label]
        elif operation == '=':
            boxes[index][label] = focal_length
    return sum((box_i + 1) * focusing_power(box) for box_i, box in boxes.items())

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve1(puzzle))
    print('part2', solve2(puzzle))
