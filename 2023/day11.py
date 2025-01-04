from day import Day
from grid import Grid

class Day11(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)

    def part1(self):
        def expand_grid(grid):
            rows_to_expand = [i for i, row in enumerate(grid) if '#' not in row]
            columns_to_expand = []
            for col in range(len(grid[0])):
                if all(row[col] == '.' for row in grid):
                    columns_to_expand.append(col)

            expanded_grid = []
            for i, row in enumerate(grid):
                expanded_grid.append(row)
                if i in rows_to_expand:
                    expanded_grid.append(row)

            final_grid = []
            for row in expanded_grid:
                new_row = []
                for j, char in enumerate(row):
                    new_row.append(char)
                    if j in columns_to_expand:
                        new_row.append(char)
                final_grid.append(''.join(new_row))

            return final_grid

        self.grid = Grid(self.input.rows_listed(expand_grid(self.rows)))
        self.galaxies = self.grid.get_elem_pos('#')
        self.grid_map = {}
        id = 1
        self.galaxies_ids = {}
        for galaxy in self.galaxies:
            self.grid_map[galaxy] = id
            self.galaxies_ids[id] = galaxy
            id += 1

        def manhattan_distance(start, end):
            return sum(abs(a - b) for a, b in zip(start, end))

        def all_distances(galaxy, visited):
            costs = 0
            id = int(self.grid_map[galaxy])
            for key , galaxy2 in self.galaxies_ids.items():
                if galaxy != galaxy2 and not galaxy2 in visited:
                    cost = manhattan_distance(galaxy, galaxy2)
                    costs += cost
            return costs

        res = 0
        visited = set()
        for _ , galaxy in self.galaxies_ids.items():
                visited.add(galaxy)
                res += all_distances(galaxy, visited)

        return res

    def part2(self):
        def expand_grid(grid):
            self.rows_to_expand = [i for i, row in enumerate(grid) if '#' not in row]
            for col in range(len(grid[0])):
                if all(row[col] == '.' for row in grid):
                    self.columns_to_expand.append(col)

        def manhattan_distance(start, end, expansion):
            xs , ys = start
            xe , ye = end
            expanded = 0
            x_min = min(xs, xe)
            x_max = max(xs, xe)
            y_min = min(ys, ye)
            y_max = max(ys, ye)
            for i in self.rows_to_expand:
                if i >= x_min and i <= x_max:
                    expanded += 1
            for j in self.columns_to_expand:
                if j >= y_min and j <= y_max:
                    expanded += 1

            return sum(abs(a - b) for a, b in zip(start, end)) + (expanded * expansion)

        def all_distances(galaxy, visited, expansion):
            costs = 0
            id = int(self.grid_map[galaxy])
            for key , galaxy2 in self.galaxies_ids.items():
                if galaxy != galaxy2 and not galaxy2 in visited:
                    cost = manhattan_distance(galaxy, galaxy2, expansion)
                    costs += cost
            return costs

        res = 0
        visited = set()
        self.rows_to_expand = []
        self.columns_to_expand = []
        expand_grid(self.rows)
        self.grid = Grid(self.input.rows_listed(self.rows))
        self.galaxies = self.grid.get_elem_pos('#')
        self.grid_map = {}
        id = 1
        self.galaxies_ids = {}
        for galaxy in self.galaxies:
            self.grid_map[galaxy] = id
            self.galaxies_ids[id] = galaxy
            id += 1

        # one expansion are two rows, therefore 9 expanssions are 10 rows, and so on
        for _ , galaxy in self.galaxies_ids.items():
                visited.add(galaxy)
                res += all_distances(galaxy, visited, 999999)

        return res