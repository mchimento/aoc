from day import Day
import copy
class Day07(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        rows = []
        self.rows = self.input.process_data_as_rows(0)
        for row in self.rows:
            parts = row.split(':')
            test = int(parts[0].strip())
            values = [int(num) for num in parts[1].strip().split()]
            result = (test, values)
            rows.append(result)
        self.rows = rows
        print(self.rows)

    def add(self, x, y):
            return x+y
    def mult(self, x, y):
        return x*y
    def app(self, x, y):
        return int(str(x)+str(y))
    def eval_all_exps(self, values, operations):
        if len(values) == 1:
            return values
        val = values.pop()
        rec = self.eval_all_exps(values, operations)
        exps = []
        for op in operations:
            for exp in rec:
                exps.append(op(exp, val))
        return exps

    def part1(self):
        operations = [self.add, self.mult]
        res = 0
        rows_part1 = copy.deepcopy(self.rows)
        for row in rows_part1:
            if row[0] in self.eval_all_exps(row[1], operations):
                res += row[0]
        return res

    def part2(self):
        operations = [self.add, self.mult, self.app]
        res = 0
        for row in self.rows:
            if row[0] in self.eval_all_exps(row[1], operations):
                res += row[0]
        return res
