from day import Day
import re

class Day19(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.patterns = self.input.process_data_as_rows(0)
        self.patterns = list(map(lambda x : x.strip(), self.patterns[0].split(",")))
        self.designs = self.input.process_data_as_rows(1)

    def get_valid_patterns(self, design):
        found = []
        for pattern in self.patterns:
            founded = re.search(pattern, design)
            if founded is not None:
                found.append(pattern)
        return found

    def part1(self):
        def check_towels(design, patterns):
            size = len(design)
            dp = [False for x in range(size+1)]
            dp[0] = True

            for i in range(1, size + 1):
                for pattern in patterns:
                    if dp[i - len(pattern)] and design[i - len(pattern):i] == pattern:
                        dp[i] = True
                        break
            return dp[size]

        ret = 0
        for design in self.designs:
            patterns = self.get_valid_patterns(design)
            if check_towels(design, patterns):
                ret += 1
        return ret

    def part2(self):
        def count_design(design, patterns):
            size = len(design)
            dp = [0 for x in range(size+1)]
            dp[0] = 1

            for i in range(1, size + 1):
                for pattern in patterns:
                    if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                        dp[i] += dp[i - len(pattern)]
            return dp[size]

        ret = 0
        for design in self.designs:
            patterns = self.get_valid_patterns(design)
            ret += count_design(design, patterns)
        return ret