from day import Day
from directions import Directions
from collections import deque

class Day18(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        parsed = []
        self.rows = self.input.process_data_as_rows(0)
        for row in self.rows:
            parse = self.input.int_list(row.split(','))
            parsed.append(parse)
        self.rows = parsed
        self.grid = []
        self.dirs = Directions(self.grid, wall="#", empty=".")

    def create_grid(self, size):
        if self.grid:
            self.grid = []
        for _ in range(size):
            self.grid.append([self.dirs.empty for _ in range(size)])

    def shortest_path(self):
        rows, cols = len(self.grid), len(self.grid[0])
        visited = set()
        parent = {}
        queue = deque([(0, 0, 0, self.dirs.right)])  # (x, y, distance, dir)

        while queue:
            x, y, dist , dir = queue.popleft()
            if (x, y) == (cols - 1, rows - 1):
                path = []
                current = (x, y, dir)
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                return dist, path[::-1]
            visited.add((x, y, dir))
            for d in self.dirs.directions:
                nx, ny , ndir = self.dirs.move_from(x, y, d)
                if (nx, ny, ndir) not in visited and self.grid[nx][ny] != self.dirs.wall:
                    queue.append((nx, ny, dist + 1, ndir))
                    visited.add((nx, ny, ndir))
                    if (nx, ny) not in parent:
                        parent[(nx, ny, ndir)] = (x, y, dir)
        return None , None

    def part1(self):
        def drop_bytes(limit=None):
            i = 0
            for x , y in self.rows:
                if limit is not None and i==limit:
                    break
                i+=1
                self.grid[y][x] = self.dirs.wall

        self.create_grid(71)
        print(self.grid)
        drop_bytes(1024)
        dist , _ = self.shortest_path()
        return dist

    def part2(self):
        def first_block():
            _ , path = self.shortest_path()
            while path is not None and self.rows:
                x , y = self.rows.pop(0)
                self.grid[y][x] = self.dirs.wall
                _ , path = self.shortest_path()
            return x , y

        self.create_grid(71)
        return first_block()