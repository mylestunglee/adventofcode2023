import sys
from collections import namedtuple, defaultdict, Counter, deque
import math

Module = namedtuple('Module', ['type', 'targets'])
Pulse = namedtuple('Pulse', ['type', 'prev', 'curr'])

MODULE_NAME_BROADCASTER = 'broadcaster'
MODULE_TYPE_BROADCASTER = 'broadcaster'
MODULE_TYPE_FLIP_FLOP = 'flip-flop'
MODULE_TYPE_CONJUNCTION = 'conjunction'
FLIP_FLOP_OFF = False
FLIP_FLOP_ON = True
PULSE_LOW = False
PULSE_HIGH = True

def parse_config_input(config_input):
    config = {}
    all_targets = []
    for line in config_input.rstrip().split('\n'):
        left, right = line.split(' -> ')
        if left == MODULE_NAME_BROADCASTER:
            module_type = MODULE_TYPE_BROADCASTER
            name = left
        elif left[0] == '%':
            module_type = MODULE_TYPE_FLIP_FLOP
            name = left[1:]
        elif left[0] == '&':
            module_type = MODULE_TYPE_CONJUNCTION
            name = left[1:]
        else:
            module_type = None
            name = left
        targets = list(right.split(', '))
        all_targets += targets
        config[name] = Module(module_type, targets)
    for target in all_targets:
        if not target in config:
            config[target] = Module(None, [])
    return config

def initial_flip_flop_states(config):
    return {name: FLIP_FLOP_OFF for name, module in config.items() if module.type == MODULE_TYPE_FLIP_FLOP}

def initial_conjunction_states(config):
    states = defaultdict(lambda: {})
    for source_name, source_module in config.items():
        for target_name in source_module.targets:
            if not target_name in config:
                continue
            target_module = config[target_name]
            if target_module.type == MODULE_TYPE_CONJUNCTION:
                states[target_name][source_name] = PULSE_LOW
    return dict(states)

def all_high(conjunction_state):
    return all(pulse_type == PULSE_HIGH for source, pulse_type in conjunction_state.items())

def simulate(config, flip_flop_states, conjunction_states):
    pulses = deque()
    pulses.append(Pulse(PULSE_LOW, None, MODULE_NAME_BROADCASTER))
    subcounters = {name: Counter() for name in config}

    while pulses:
        pulse_type, prev, curr = pulses.popleft()

        subcounters[curr][pulse_type] += 1

        module = config[curr]

        def fire(pulse_type):
            for target in module.targets:
                pulses.append(Pulse(pulse_type, curr, target))

        if module.type == MODULE_TYPE_BROADCASTER:
            fire(pulse_type)
        elif module.type == MODULE_TYPE_FLIP_FLOP:
            if pulse_type == PULSE_LOW:
                prev_state = flip_flop_states[curr]
                flip_flop_states[curr] = not flip_flop_states[curr]
                if prev_state == FLIP_FLOP_OFF:
                    fire(PULSE_HIGH)
                else:
                    fire(PULSE_LOW)
        elif module.type == MODULE_TYPE_CONJUNCTION:
            conjunction_states[curr][prev] = pulse_type
            fire(PULSE_LOW if all_high(conjunction_states[curr]) else PULSE_HIGH)

    return flip_flop_states, conjunction_states, subcounters

def solve_part1(config):
    flip_flop_states = initial_flip_flop_states(config)
    conjunction_states = initial_conjunction_states(config)
    counter = Counter()
    for _ in range(1000):
        flip_flop_states, conjunction_states, subcounters = simulate(config, flip_flop_states, conjunction_states)
        for subcounter in subcounters.values():
            counter += subcounter
    return counter[PULSE_LOW] * counter[PULSE_HIGH]

def traverse_config(config, start):
    visited = {MODULE_NAME_BROADCASTER}
    stack = deque()
    stack.append(start)
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        for target in config[curr].targets:
            stack.append(target)
    return visited

def filter_config(visited, config):
    return {name: Module(module.type, [target for target in module.targets if target in visited]) for name, module in config.items() if name in visited}

def partition_config(config):
    return [filter_config(traverse_config(config, start), config) for start in config[MODULE_NAME_BROADCASTER].targets]

def simulate_until_low_pulse(end, config):
    flip_flop_states = initial_flip_flop_states(config)
    conjunction_states = initial_conjunction_states(config)
    steps = 1
    while True:
        flip_flop_states, conjunction_states, subcounters = simulate(config, flip_flop_states, conjunction_states)
        if subcounters[end][PULSE_LOW] >= 1:
            return steps
        steps += 1

def solve_part2(config):
    steps = []
    for subconfig in partition_config(config):
        steps.append(simulate_until_low_pulse('rx', subconfig))
    return math.lcm(*steps)

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        config_input = file.read()

    config = parse_config_input(config_input)
    print('part1', solve_part1(config))
    print('part2', solve_part2(config))
