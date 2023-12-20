import sys

def parse_puzzle_input(puzzle_input):
    pass

def solve_part1(puzzle):
    pass

def solve_part2(puzzle):
    pass

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(puzzle))
    #print('part2', solve_part2(puzzle))
