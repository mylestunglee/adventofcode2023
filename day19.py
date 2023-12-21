import sys
import math
from collections import namedtuple

def parse_workflows_input(workflows_input):
    workflows = {}
    Rule = namedtuple('Rule', ['condition', 'target'])
    Condition = namedtuple('Condition', ['category', 'operand', 'value'])
    for workflow_input in workflows_input.strip().split('\n'):
        name, rules_input = workflow_input[:-1].split('{')
        rules = []
        for rule_input in rules_input.split(','):
            if ':' in rule_input:
                condition_input, target = rule_input.split(':')
                for operand in ['>', '<']:
                    if operand in condition_input:
                        category, value_input = condition_input.split(operand)
                        value = int(value_input)
                        condition = Condition(category, operand, value)
                        break
            else:
                condition = None
                target = rule_input
            rules.append(Rule(condition, target))
        workflows[name] = rules
    return workflows

def parse_parts_input(parts_input):
    parts = []
    for line in parts_input.strip().split('\n'):
        part = {}
        for category_value in line[1:-1].split(','):
            category, value_input = category_value.split('=')
            value = int(value_input)
            part[category] = value
        parts.append(part)
    return parts

def parse_puzzle_input(puzzle_input):
    workflows_input, parts_input = puzzle_input.split('\n\n')
    return parse_workflows_input(workflows_input), parse_parts_input(parts_input)

def evaluate_condition(part, condition):
    if condition is None:
        return True
    if condition.operand == '>':
        return part[condition.category] > condition.value
    if condition.operand == '<':
        return part[condition.category] < condition.value
    assert False

def evaluate_workflow(part, workflow):
    for rule in workflow:
        if evaluate_condition(part, rule.condition):
            return rule.target
    assert False

def accepted(part, workflows):
    target = 'in'
    while not target in ['A', 'R']:
        target = evaluate_workflow(part, workflows[target])
    return target == 'A'

def solve_part1(workflows, parts):
    return sum(sum(part.values()) for part in parts if accepted(part, workflows))

def is_empty(part_space):
    return any(start > end for start, end in part_space.values())

def size(part_space):
    return math.prod(end - start for start, end in part_space.values())

def split_part_space(part_space, condition):
    if condition is None:
        return part_space, {}
    positive = part_space.copy()
    negative = part_space.copy()
    start, end = part_space[condition.category]
    if condition.operand == '>':
        positive[condition.category] = (max(start, condition.value + 1), end)
        negative[condition.category] = (start, min(end, condition.value + 1))
    elif condition.operand == '<':
        positive[condition.category] = (start, min(end, condition.value))
        negative[condition.category] = (max(start, condition.value), end)
    else:
        assert False
    return positive, negative

def accepted_part_space(part_space, workflows, target):
    if is_empty(part_space):
        return 0

    if target == 'A':
        return size(part_space)

    if target == 'R':
        return 0

    accepted = 0
    for rule in workflows[target]:
        positive, part_space = split_part_space(part_space, rule.condition)
        accepted += accepted_part_space(positive, workflows, rule.target)
    return accepted

def solve_part2(workflows):
    return accepted_part_space({category: (1, 4001) for category in 'xmas'}, workflows, 'in')

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        puzzle_input = file.read()

    puzzle = parse_puzzle_input(puzzle_input)
    print('part1', solve_part1(*puzzle))
    print('part2', solve_part2(puzzle[0]))
