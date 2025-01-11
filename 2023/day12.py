from day import Day
from functools import cache

class Day12(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_zip_rows(0)
        self.springs = list(map(lambda row : (row[0], tuple(self.input.int_list(row[1].split(',')))), input))

    @cache
    def num_solutions(self, s, sizes, num_done_in_group=0):
        if not s:
            # Is this a solution? Did we handle and close all groups?
            return not sizes and not num_done_in_group
        num_sols = 0
        # If next letter is a "?", we branch
        possible = [".", "#"] if s[0] == "?" else s[0]
        for c in possible:
            if c == "#":
                # Extend current group
                num_sols += self.num_solutions(s[1:], sizes, num_done_in_group + 1)
            else:
                if num_done_in_group:
                    # If we were in a group that can be closed, close it
                    if sizes and sizes[0] == num_done_in_group:
                        num_sols += self.num_solutions(s[1:], sizes[1:])
                else:
                    # If we are not in a group, move on to next symbol
                    num_sols += self.num_solutions(s[1:], sizes)
        return num_sols

    def part1(self):
        res = 0
        for spring , data in self.springs:
            res += self.num_solutions(spring + ".", data)
        return res

    def part2(self):
        res = 0
        for spring , data in self.springs:
            res += self.num_solutions("?".join([spring] * 5) + ".", data * 5)
        return res