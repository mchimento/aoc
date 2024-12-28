from day import Day
from collections import defaultdict
import math

class Day08(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.nodes = defaultdict(list)
        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))

        for i in range(len(self.rows)):
            for j in range(len(self.rows[0])):
                if self.rows[i][j] != ".":
                    self.nodes[self.rows[i][j]].append((i,j))

    def part1(self):
        antinodes = set()
        def check_antinode(pr1, pr2):
            x1, y1 = pr1
            x2, y2 = pr2
            newx = x2 + (x2 - x1)
            newy = y2 + (y2 - y1)
            if newx >= 0 and newx < len(self.rows) and newy >= 0 and newy < len(self.rows[0]):
                antinodes.add((newx,newy))

        for node in self.nodes:
            nodes = self.nodes[node]
            for i in range(len(nodes)):
                for j in range(i):
                    node1 = nodes[i]
                    node2 = nodes[j]
                    check_antinode(node1, node2)
                    check_antinode(node2, node1)
        return len(antinodes)

    def part2(self):
        antinodes = set()
        def check_antinode(pr1, pr2):
            x1, y1 = pr1
            x2, y2 = pr2
            dx, dy = x2 - x1, y2 - y1
            gcd = abs(math.gcd(dx, dy))
            step_x, step_y = dx // gcd, dy // gcd
            for direction in (-1, 1):  # Backward (-1) and forward (1) extensions
                px, py = x1, y1
                while 0 <= px < len(self.rows) and 0 <= py < len(self.rows):
                    antinodes.add((px, py))
                    px += direction * step_x
                    py += direction * step_y
            """
            newx = x2 + (x2 - x1)
            newy = y2 + (y2 - y1)
            while newx >= 0 and newx < len(self.rows) and newy >= 0 and newy < len(self.rows[0]):
                antinodes.add((newx,newy))
                newx += (x2 - x1)
                newy += (y2 - y1)
            """
        for node in self.nodes:
            nodes = self.nodes[node]
            for i in range(len(nodes)):
                for j in range(i):
                    node1 = nodes[i]
                    node2 = nodes[j]
                    check_antinode(node1, node2)
                    check_antinode(node2, node1)
        return len(antinodes)