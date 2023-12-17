puzzle_input = open('input11_2.txt').read()

def get_positions(input):
	return [(x, y) for y, line in enumerate(input.split('\n')) for x, char in enumerate(line) if char == '#']

def get_axis_set(positions, index):
	return {position[index] for position in positions}

def get_axis_map(zs, scale):
	z_max = max(zs)
	result = {}
	offset = 0
	for i in range(z_max + 1):
		if i in zs:
			result[i] = i + offset
		else:
			offset += scale - 1
	return result

def map_positions(positions, x_map, y_map):
	return [(x_map[x], y_map[y]) for x, y in positions]

def distance(p, q):
	return sum(abs(a - b) for a, b in zip(p, q))

def sum_distances(positions):
	return sum(distance(p, q) for i, p in enumerate(positions) for j, q in enumerate(positions) if i < j)

def solve(puzzle_input, scale):
	positions = get_positions(puzzle_input)
	x_map = get_axis_map(get_axis_set(positions, 0), scale)
	y_map = get_axis_map(get_axis_set(positions, 1), scale)
	expanded = map_positions(positions, x_map, y_map)
	return sum_distances(expanded)

print('part1', solve(puzzle_input, 2))
print('part2', solve(puzzle_input, 1000000))
