import sys

def parse_puzzle_input(puzzle_input):
    puzzle = []
    for line in puzzle_input.strip().split('\n'):
        row, lengths_input = line.split(' ')
        lengths = [int(length) for length in lengths_input.split(',')]
        puzzle.append((row, lengths))
    return puzzle

def unfold_puzzle(puzzle):
    return [('?'.join([row] * 5), lengths * 5) for row, lengths in puzzle]

def split_row(row):
    for i, char in enumerate(row):
        if char == '.' or char == '?':
            yield row[:i], '.', row[i + 1:]
            unsplit = False
    yield row, '', ''

def spring_arrangements_at_end(row, length):
    if len(row) >= length and all(char in ['.', '?'] for char in row[:-length]) and all(char in ['#', '?'] for char in row[-length:]):
        return 1 # Place spring at end of row
    else:
        return 0 # Failed to sub

# Recursive by breaking down a screw length at a time
def spring_arrangements(row, lengths, cache):
    cached = cache.get((row, tuple(lengths)))
    if not cached is None:
        return cached
    if not row and lengths:
        return 0 # Cannot fit screw into empty row
    if not row and not lengths:
        return 1
    if row and not lengths:
        # Attempt to sub all ? with .
        if all(char in ['.', '?'] for char in row):
            return 1
        else:
            return 0 # Failed to sub
    if all(char == '.' for char in row) and lengths:
        return 0 # Cannot fit any screws into blanks
    if len(row) < sum(lengths) + len(lengths) - 1:
        return 0 # Cannot arrange screws in row to meet lengths

    arrangements = 0
    for left_subrow, delimitor, right_subrow in split_row(row):
        left_arrangements = spring_arrangements_at_end(left_subrow, lengths[0])
        if left_arrangements > 0:
            arrangements += spring_arrangements(right_subrow, lengths[1:], cache)
    cache[(row, tuple(lengths))] = arrangements
    return arrangements

def solve(puzzle):
    count = 0
    for row, lengths in puzzle:
        cache = {}
        arrangements = spring_arrangements(row, lengths , cache)
        count += arrangements
    return count

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve(puzzle))
    print('part2', solve(unfold_puzzle(puzzle)))
