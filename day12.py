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
        if (char == '.' and (i == 0 or not row[i - 1] == '.')) or char == '?':
            yield row[:i], row[i + 1:]

def split_lengths(lengths):
    for i in range(len(lengths) + 1):
        yield lengths[:i], lengths[i:]

def spring_arrangements(row, lengths, cache):
    cached = cache.get((row, tuple(lengths)))
    if not cached is None:
        return cached
    
    if len(row) < sum(lengths) + len(lengths) - 1:
        return set() # Cannot arrange screws in row to meet lengths

    if not lengths:
        if any(char == '#' for char in row):
            return set() # Not possible to have 0 screws with a #
        else:
            return {'.' * len(row)} # Sub all ? with .

    if lengths == [len(row)] and all(char == '?' or char == '#' for char in row):
        return {'#' * len(row)} # Sub all ? with #

    row_subs = set()
    for left_row, right_row in split_row(row):
        for left_lengths, right_lengths in split_lengths(lengths):
            left_row_subs = spring_arrangements(left_row, left_lengths, cache)
            right_row_subs = spring_arrangements(right_row, right_lengths, cache)
            for left_row_sub in left_row_subs:
                for right_row_sub in right_row_subs:
                    row_sub = left_row_sub + '.' + right_row_sub # Sub split with .
                    row_subs.add(row_sub)
    cache[(row, tuple(lengths))] = row_subs
    return row_subs

def solve(puzzle):
    count = 0
    for row, lengths in puzzle:
        print(row, lengths)
        arragements = spring_arrangements(row, lengths, {})
        count += len(arragements)
        print(len(arragements))
    return count

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve(puzzle))
    print('part1', solve(unfold_puzzle(puzzle)))
