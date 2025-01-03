from day import Day
from grid import Grid

class Day03(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_listed_rows(0)
        self.grid = Grid(input)
        self.coord = {}

    def get_digits(self, i):
        numbers = []
        digit = []
        for y in range(self.grid.width()):
            if self.grid.get(i, y).isdigit():
                digit.append((i, y))
            else:
                if not digit:
                    continue
                numbers.append(digit)
                digit = []
            if y == self.grid.width() - 1 and digit:
                numbers.append(digit)
        return numbers

    def part1(self):
        all_numbers = []
        def check_digits(digits):
            visited = set()
            def get_diagonal(x, y):
                diag = []
                for x , y in [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)]:
                    if x >= 0 and x < self.grid.height() and y >= 0 and y < self.grid.width():
                        diag.append((x, y))
                return diag
            for digit in digits:
                reachables = self.grid.reachable_nodes(digit[0], digit[1])
                reachables += get_diagonal(digit[0], digit[1])
                reachables = set(reachables) - visited
                for x, y in reachables:
                    if not self.grid.get(x, y).isdigit() and self.grid.get(x, y) != ".":
                        return True
                visited.add(digit)
                visited = visited.union(set(reachables))
            return False

        for i in range(self.grid.height()):
            all_numbers += self.get_digits(i)

        res = 0
        for number in all_numbers:
            if check_digits(number):
                num = ""
                for digit in number:
                    num += self.grid.get(digit[0], digit[1])
                res += int(num)
                for digit in number:
                    self.coord[digit] = int(num)

        return res

    def part2(self):
        all_numbers = []
        def check_gear(x, y):
            def get_diagonal(x, y):
                diag = []
                for x , y in [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)]:
                    if x >= 0 and x < self.grid.height() and y >= 0 and y < self.grid.width():
                        diag.append((x, y))
                return diag
            reachables = self.grid.reachable_nodes(x, y)
            reachables += get_diagonal(x, y)
            touches = set()
            for node in reachables:
                if (node[0], node[1]) in self.coord:
                    touches.add(self.coord[node])

            if len(touches) == 2:
                xs = list(touches)
                prod = xs[0] * xs[1]
                return True , prod
            return False , 0

        for i in range(self.grid.height()):
            all_numbers += self.get_digits(i)

        res = 0
        for x in range(self.grid.height()):
            for y in range(self.grid.width()):
                if self.grid.get(x, y) != '*':
                    continue
                else:
                    b , prod = check_gear(x, y)
                    if b:
                        res += prod
        return res