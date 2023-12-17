puzzle_input = open('input09_2.txt').read()

def parse_puzzle_input(puzzle_input):
	return [[int(token) for token in line.split()] for line in puzzle_input.split('\n')]

def all_zeros(nums):
	return all(num == 0 for num in nums)

def predict_forwards(nums):
	if all_zeros(nums):
		return 0
		
	return nums[-1] + predict_forwards([nums[i] - nums[i - 1] for i in range(1, len(nums))])

def predict_backwards(nums):
	if all_zeros(nums):
		return 0
		
	return nums[0] - predict_backwards([nums[i] - nums[i - 1] for i in range(1, len(nums))])

def solve1(puzzle):
	return sum(predict_forwards(nums) for nums in puzzle)

def solve2(puzzle):
	return sum(predict_backwards(nums) for nums in puzzle)

puzzle = parse_puzzle_input(puzzle_input)
print('part1', solve1(puzzle))
print('part2', solve2(puzzle))
