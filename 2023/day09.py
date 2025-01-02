from day import Day
from functools import reduce

class Day09(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_rows(0)
        self.histories = []
        for line in input:
            self.histories.append(self.input.int_list(line.split()))

    def part1(self):
        def diff_history(history):
            return  [history[i] - history[i-1] for i in range(1, len(history))]

        def next_value(history):
            if all(val == 0 for val in history):
                return 0
            last = history[-1]
            diff_h = diff_history(history)
            return last + next_value(diff_h)

        res = 0
        for history in self.histories:
            res += next_value(history)

        return res

    def part2(self):
        def diff_history(history):
            return  [history[i] - history[i-1] for i in range(1, len(history))]

        def prev_value(history):
            if all(val == 0 for val in history):
                return 0
            first = history[0]
            diff_h = diff_history(history)
            return first - prev_value(diff_h)

        res = 0
        for history in self.histories:
            res += prev_value(history)

        return res