from day import Day

class Day02(Day):

    def __init__(self):
        self.grid = []
        super().__init__()

    def parse_input(self):
        lines = self.input.process_data_as_rows(0)
        for line in (lines):
            self.grid.append(self.input.int_list(line.strip().split(' ')))

    def part1(self):
       def is_sorted_ascending(xs):
           return all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1))
       def is_sorted_descending(xs):
           return all(xs[i] >= xs[i + 1] for i in range(len(xs) - 1))
       def is_safe(xs):
           return all(1 <= abs(xs[i] - xs[i + 1]) <= 3 for i in range(len(xs) - 1))
       def is_sorted(xs):
           return is_sorted_ascending(xs) or is_sorted_descending(xs)
       res = 0
       for row in self.grid:
           if is_safe(row) and is_sorted(row):
               res += 1
       return res

    def part2(self):
       def is_sorted_ascending(xs):
           return all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1))
       def is_sorted_descending(xs):
           return all(xs[i] >= xs[i + 1] for i in range(len(xs) - 1))
       def is_safe(xs):
           return all(1 <= abs(xs[i] - xs[i + 1]) <= 3 for i in range(len(xs) - 1))
       def is_sorted(xs):
           return is_sorted_ascending(xs) or is_sorted_descending(xs)
       def dampener(n, xs):
            damped = xs[:n] + xs[n+1:]
            if n + 1 == len(xs):
               return is_safe(damped) and is_sorted(damped)
            else:
               rec = dampener(n + 1, xs)
               return is_safe(damped) and is_sorted(damped) or rec
       res = 0
       for row in self.grid:
            if is_safe(row) and is_sorted(row):
               res += 1
            else:
                if dampener(0, row):
                   res += 1
       return res