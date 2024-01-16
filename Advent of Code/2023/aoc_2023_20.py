import re
from collections import defaultdict, deque

with open("data/aoc_input_2023_20.txt") as file:
    file_contents = file.read()


class Module:
    low_count = 0
    high_count = 0

    def __init__(self, label, *args):
        self.label = label
        self.output_destinations = args

    def output(self, signal='low'):
        if signal == 'low':
            Module.low_count += len(self.output_destinations)
        if signal == 'high':
            Module.high_count += len(self.output_destinations)

        return [(od, signal, self.label) for od in self.output_destinations]


class FlipFlop(Module):
    def __init__(self, label, *args):
        super().__init__(label, *args)
        self.state = 'off'

    def receive_pulse(self, pulse, source):
        emit_signal = None
        if pulse == 'low':
            if self.state == 'off':
                self.state = 'on'
                emit_signal = 'high'
            elif self.state == 'on':
                self.state = 'off'
                emit_signal = 'low'

        if emit_signal is not None:
            return self.output(emit_signal)

    def __str__(self):
        return f'FlipFlop({self.label=}, {self.state=}, {self.output_destinations=})'


class Conjunction(Module):
    def __init__(self, label, *args):
        super().__init__(label, *args)
        self.memory = defaultdict(lambda: 'low')

    def receive_pulse(self, pulse, source):
        self.memory[source] = pulse

        if all(mem == 'high' for mem in self.memory.values()):
            emit_signal = 'low'
        else:
            emit_signal = 'high'

        return self.output(emit_signal)


def broadcast_push():
    Module.low_count += 1
    pulse_queue = deque(broadcaster.output())

    while pulse_queue:
        mod_label, pulse, source = pulse_queue.popleft()
        if mod_label not in modules:
            # print(f'{mod_label} is {pulse}')
            if mod_label == 'rx' and pulse == 'low':
                return True
        else:
            module = modules[mod_label]
            output_pulses = module.receive_pulse(pulse, source)
            if output_pulses is not None:
                pulse_queue.extend(output_pulses)


broadcaster_match = re.search(r"broadcaster.->.(.+)", file_contents)
broadcaster = Module("broadcaster", *broadcaster_match.group(1).split(', '))

flipflop_matches = re.findall(r"%([a-z]+).->.(.*)", file_contents)
conjunction_matches = re.findall(r"&([a-z]+).->.(.*)", file_contents)
flipflops = {label: FlipFlop(label, *destination_string.split(', '))
             for label, destination_string in flipflop_matches}
conjunctions = {label: Conjunction(label, *destination_string.split(', '))
                for label, destination_string in conjunction_matches}
modules = dict(flipflops, **conjunctions)

for mod in modules.values():
    for destination in mod.output_destinations:
        if destination not in modules:
            continue
        if isinstance(modules[destination], Conjunction):
            modules[destination].memory[mod.label] = 'low'


rx_stop = False
count = 0
while not rx_stop:
    rx_stop = broadcast_push()
    count += 1
    if count % 100 == 0:
        print(count)

# print(f'Solution to Day 20, problem 1 is {Module.low_count * Module.high_count}')
