from day import Day
from input import Input

class Day6(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.input1 = self.input.process_data_as_zip_columns(0)

    def calc(self, x, y, symbol):
        if symbol == '+':
            return int(x) + int(y)
        else:
            return int(x) * int(y)

    def process_data_as_zip_columns_aux(self, file_ix):
        rows = self.input.process_data_as_rows(file_ix, False)
        if rows is None:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None
        else:
            symbols = rows[-1]
            cuts = []
            for ix in range(1, len(symbols)):
                if symbols[ix] != ' ':
                    cuts.append(ix)            
            def slice_at(s, start, end):
                xs = []
                for ix in range(start, end):
                    xs.append(s[ix])
                return xs

            split_rows = []
            for row in rows:
                prev = 0
                slices = []                
                for ix in cuts:
                    row_slice = slice_at(row, prev, ix-1)
                    prev = ix
                    slices.append(row_slice)
                slices.append(slice_at(row, prev, len(row)))
                split_rows.append(slices)

            if not split_rows:
                return []
            
            return list(zip(*split_rows))

    def part1(self):
        total = 0
        for problem in self.input1:
            symbol = problem[-1]
            ret = 0
            for ix in range(1, len(problem)-1):
                x = problem[ix-1] if ix-1 == 0 else ret
                y = problem[ix]
                ret = self.calc(x, y, symbol)
            total += ret
        return total

    def part2(self):
        total = 0
        self.input = self.process_data_as_zip_columns_aux(0)
        for problem in self.input:
            p = list(problem)
            symbol = "".join(p.pop(-1)).strip()
            def concat_columns(xs):
                return [''.join(column).strip() for column in zip(*xs)]
            
            p = concat_columns(p)
            ret = 0
            for ix in range(1, len(p)):
                x = p[ix-1] if ix-1 == 0 else ret
                y = p[ix]
                ret = self.calc(x, y, symbol)
            total += ret

        return total