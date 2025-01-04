from day import Day
from grid import Grid
from directions import Directions
import heapq

class Day11(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        rows = self.input.process_data_as_rows(0)
        empty_rows = set()
        empty_cols = set()
        for i , row in enumerate(rows):
            if all(x == '.' for x in row):
                empty_rows.add(i)
        ext = 0
        for ix in empty_rows:
            rows.insert(ix + ext, '.' * len(rows[0]))
            ext += 1
        ext = 0
        columns = [''.join(column) for column in zip(*rows)]
        for j , col in enumerate(columns):
            if all(x == '.' for x in col):
                empty_cols.add(j)
        for ix in empty_cols:
            columns.insert(ix + ext, '.' * len(columns[0]))
            ext += 1
        rows = [list(row) for row in zip(*columns)]

        self.grid = Grid(self.input.rows_listed(rows))
        self.galaxies = self.grid.get_elem_pos('#')
        id = 0
        self.galaxies_ids = {}
        for galaxy in self.galaxies:
            self.grid[galaxy] = id
            self.galaxies_ids[id] = galaxy
            id += 1
        self.grid.print_grid()

    def part1(self):
        def shortest_paths(start, end, galaxy):
            """
            General shortest path algorithm
            """
            pq = []
            parent = {}
            heapq.heappush(pq, (0, start[0], start[1]))  # (cost, x, y)
            visited = set()
            dirs = Directions()

            rows , cols = self.grid.height()-1 , self.grid.width()-1

            while pq:
                cost, x, y = heapq.heappop(pq)

                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if self.grid[x, y] == end:
                    all_paths = []
                    reconstruct_paths(x, y, start, parent, all_paths, [(x, y)])
                    all_paths = list(map(lambda xs: xs[::-1], all_paths))
                    return cost, all_paths

                for d in dirs.directions:
                    dx , dy = dirs.coord(d)
                    nx, ny = x + dx , y + dy
                    if 0 <= nx <= rows and 0 <= ny <= cols \
                        and (nx, ny) not in visited \
                        and self.grid[nx, ny] != dirs.wall:
                        heapq.heappush(pq, (cost + 1, nx, ny))
                        if (nx, ny) not in parent:
                            parent[(nx, ny)] = []
                        parent[(nx, ny)].append((x, y))

            return None, []

        def reconstruct_paths(x, y, start, parent, all_paths, current_path):
            if (x, y) == (start[0], start[1]):
                all_paths.append(list(current_path))
                return
            if (x, y) in parent:
                for px, py in parent[(x, y)]:
                    current_path.append((px, py))
                    reconstruct_paths(px, py, start, parent, all_paths, current_path)
                    current_path.pop()

        def galaxies_shortest_paths(galaxy, visited):
            costs = 0
            id = int(self.grid[galaxy])
            for key , galaxy2 in self.galaxies_ids.items():
                if galaxy != galaxy2 and not galaxy2 in visited:
                    if (id, key) in self.path_cache:
                        cost = self.path_cache[(galaxy, galaxy2)]
                    elif (key, id) in self.path_cache:
                        cost = self.path_cache[(galaxy, galaxy2)]
                    else:
                        cost , _ = shortest_paths(galaxy, str(key), galaxy2)
                        self.path_cache[(id, key)] = cost
                        self.path_cache[(key, id)] = cost
                    costs += cost
            return costs

        self.path_cache = {}
        res = 0
        visited = set()
        for key , galaxy in self.galaxies_ids.items():
                visited.add(galaxy)
                res += galaxies_shortest_paths(galaxy, visited)

        print(self.path_cache)

        return res

    def part2(self):
        return super().part2()