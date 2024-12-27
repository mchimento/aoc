from day import Day

class Day01(Day):
    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.column1 = []
        self.column2 = []
        lines = self.input.process_data_as_rows(0)
        for line in (lines):
            c1 , c2 = line.strip().split('  ')
            self.column1.append(c1)
            self.column2.append(c2)
        self.column1 = self.input.int_list(self.column1)
        self.column2 = self.input.int_list(self.column2)

    def part1(self):
        col0 = sorted(self.column1)
        col1 = sorted(self.column2)
        res = sum([abs(y-x) for x, y in zip(col0, col1)])
        return res

    def part2(self):
        col0 = self.column1
        col1 = self.column2
        res = 0
        for x in col0:
            hit = 0
            for y in col1:
                if x == y:
                    hit += 1
            res += x * hit
        return res