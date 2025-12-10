from day import Day
from collections import defaultdict

class Day9(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_listed_rows(0)
        self.input = [ (int(p[0]), int(p[1])) for p in [''.join(line).split(',') for line in input] ]

    def area_rect(self, x1, y1, x2, y2):
        if x1 == x2:
            return y2 - y1 + 1
        if y1 == y2:
            return x2 - x1 + 1
        dy = abs(y1 - y2) + 1
        dx = abs(x1 - x2) + 1
        return dy * dx

    def part1(self):
        max_size = 0
        for ix , (y1, x1) in enumerate(self.input):
            for (y2, x2) in self.input[:ix+1]:
                max_size = max(self.area_rect(x1, y1, x2, y2), max_size)

        return max_size

    def orthogonal_adjacent_edges(self, points):
        edges = set()

        by_x = defaultdict(list)
        for x, y in points:
            by_x[x].append((x, y))
        for x, pts in by_x.items():
            pts_sorted = sorted(pts, key=lambda p: p[1])
            for a, b in zip(pts_sorted, pts_sorted[1:]):
                edges.add((a, b))

        by_y = defaultdict(list)
        for x, y in points:
            by_y[y].append((x, y))
        for y, pts in by_y.items():
            pts_sorted = sorted(pts, key=lambda p: p[0])
            for a, b in zip(pts_sorted, pts_sorted[1:]):
                edges.add((a, b))

        return list(edges)

    def is_fully_contained(self, edges, min_x, min_y, max_x, max_y):
        for ((e_min_x, e_min_y), (e_max_x, e_max_y)) in edges:
            if min_x < e_max_x and max_x > e_min_x and min_y < e_max_y and max_y > e_min_y:
                return False
        return True

    def part2(self):
        tiles = [(x, y) for y, x in self.input]
        edges = self.orthogonal_adjacent_edges(tiles)
        max_size = 0

        for ix , (x1, y1) in enumerate(tiles):
            for (x2, y2) in tiles[:ix+1]:

                area = self.area_rect(x1, y1, x2, y2)
                if area <= max_size:
                    continue

                # Get rectangle bounds
                min_x, max_x = (x1, x2) if x1 < x2 else (x2, x1)
                min_y, max_y = (y1, y2) if y1 < y2 else (y2, y1)

                if self.is_fully_contained(edges, min_x, min_y, max_x, max_y):
                    max_size = area

        return max_size