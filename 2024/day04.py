from day import Day
import re

class Day04(Day):

    def __init__(self):
        self.rows = []
        self.columns = []
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)
        self.columns = self.input.process_data_as_columns(0)

    def part1(self):
        def horizontal(rows, pattern):
            res = 0
            for row in rows:
                matches = re.findall(pattern, row)
                res += len(matches)
            return res
        def vertical(columns, pattern):
            res = 0
            for col in columns:
                matches = re.findall(pattern, col)
                res += len(matches)
            return res
        def mkDiagonal(rows, x, y, limit):
            if x == len(rows):
                return []
            if y == limit:
                return []
            rec = mkDiagonal(rows, x+1, y+1, limit)
            rec.append(rows[x][y])
            return rec
        def mkDiagRow(rows, x, limit):
            res = []
            for y in range(0, limit-1):
                res.append(''.join(mkDiagonal(rows, x, y, limit)[::-1]))
            return res
        def diagonal(rows, limit, pattern):
            res = []
            for x in range(0, len(rows)-1):
                res += mkDiagRow(rows, x, limit)
            ret = 0
            for xs in res:
                ret += len(re.findall(pattern, xs[:4]))
            return ret
        rows = [xs[::-1] for xs in self.rows]

        res = horizontal(self.rows, r'XMAS') \
              + vertical(self.columns, r'XMAS') \
              + diagonal(self.rows, len(self.columns), r'XMAS') \
              + diagonal(rows, len(self.columns), r'XMAS') \
              + horizontal(self.rows, r'SAMX') \
              + vertical(self.columns, r'SAMX') \
              + diagonal(self.rows, len(self.columns), r'SAMX') \
              + diagonal(rows, len(self.columns), r'SAMX')

        return res

    def part2(self):
        def mkSquares(rows):
            row0 = rows[0]
            row1 = rows[1]
            row2 = rows[2]
            limit = len(row0)
            squares = []
            for i in range(0, limit-2):
                square = list(row0[:3] + row1[:3] + row2[:3])
                row0 = row0[1:]
                row1 = row1[1:]
                row2 = row2[1:]
                squares.append(square)
            return squares
        def check_square(xs):
            diag1 = xs[0] + xs[4] + xs[8]
            diag2 = xs[2] + xs[4] + xs[6]
            diag1_mas = re.match(diag1, r'MAS') \
                        and re.match(diag2, r'SAM')
            diag2_mas = re.match(diag1, r'SAM') \
                        and re.match(diag2, r'MAS')
            diag3_mas = re.match(diag1, r'MAS') \
                        and re.match(diag2, r'MAS')
            diag4_mas = re.match(diag1, r'SAM') \
                        and re.match(diag2, r'SAM')
            res = diag1_mas or diag2_mas or diag3_mas or diag4_mas
            return res

        squares = []
        limit = len(self.rows)
        res = 0
        for i in range(0, limit-2):
            squares = mkSquares(self.rows[:3])
            for square in squares:
                if check_square(square):
                    res += 1
            self.rows.pop(0)
        return res