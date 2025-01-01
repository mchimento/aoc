from day import Day
from collections import defaultdict
import math
from functools import reduce

class Day08(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.instructions = self.input.process_data_as_listed_rows(0)[0]
        network_data = self.input.process_data_as_rows(1)
        self.network = defaultdict(dict)

        for line in network_data:
            node , edges = line.split("=")
            edges = edges.strip().strip("()").split(",")
            self.network[node.strip()] = { 'L' : edges[0].strip() , 'R' : edges[1].strip()}

    def step_count(self, start):
        count = 0
        current = start
        while not current.endswith('Z'):
            for ins in self.instructions:
                if ins == 'L':
                    current = self.network[current]['L']
                elif ins == 'R':
                    current = self.network[current]['R']
                count += 1
                if current.endswith('Z'):
                    break
        return count

    def part1(self):
        return self.step_count('AAA')

    def part2(self):
        starts = set()
        for node in self.network:
            if node.endswith('A'):
                starts.add(node)
        ends_steps = []
        ends = {}
        for node in starts:
            ends_steps.append(self.step_count(node))
            ends[node] = self.step_count(node)

        lcm = reduce(math.lcm, ends_steps)
        return lcm