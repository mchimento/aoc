from day import Day
from directions import Directions
from grid import Grid
from collections import deque , defaultdict

class Day20(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.dirs = Directions(self.rows, wall="#")
        self.path_set = set()
        self.grid = Grid(self.rows)
        self.steps_count = defaultdict(int)

    def picos_below_limit(self, picos, limit):
            count = 0
            for d in picos:
                if d >= limit:
                    count += picos[d][0]
            return count

    def reachable_nodes(self, x, y, max_dist, visited):
        reachable = []
        for dx in range(-max_dist, max_dist + 1):
            remaining_dist = max_dist - abs(dx)
            for dy in range(-remaining_dist, remaining_dist + 1):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.rows) and 0 <= ny < len(self.rows[0]) \
                    and self.rows[nx][ny] in '.SE' and not (nx, ny) in visited:
                    reachable.append((nx, ny))
        return reachable

    def check_steps(self, current, new_step):
        c_start = self.steps_count[(current[0], current[1])]
        c_end = self.steps_count[(new_step[0], new_step[1])]
        steps = c_end - c_start
        return steps

    def cheats_run(self, path, limit):
        cheats = {}
        visited = set()
        for i , step in enumerate(path):
            x , y , dir = step
            visited.add((x,y))
            nodes = self.reachable_nodes(x,y,limit,visited)
            for node in nodes:
                picoseconds = self.check_steps(step, node) - self.grid.manhattan_distance((x,y), node)
                if picoseconds in cheats:
                    a , b = cheats[picoseconds]
                    b.append(node)
                    cheats[picoseconds] = (a+1, b)
                else:
                    cheats[picoseconds] = (1, [node])
        return cheats

    def part1(self):
        def get_initial_dir(start_x, start_y):
            for d in self.dirs.directions:
                dx , dy = self.dirs.coord(d)
                nx, ny = start_x + dx , start_y + dy
                if self.rows[nx][ny] != self.dirs.wall:
                    return d

        def shortest_path(start_x, start_y, start_dir):
            rows, cols = len(self.rows), len(self.rows[0])
            visited = set()
            parent = {}
            queue = deque([(start_x, start_y, start_dir, 0)])  # (x, y, dir, distance)

            while queue:
                x, y, dir, dist = queue.popleft()
                if self.rows[x][y] == 'E':
                    path = []
                    current = (x, y, dir)
                    steps = dist
                    while current is not None:
                        path.append(current)
                        self.steps_count[(current[0], current[1])] = steps
                        steps -= 1
                        self.path_set.add((current[0], current[1]))
                        current = parent.get(current)
                    return dist, path[::-1]
                visited.add((x, y, dir))
                for d in self.dirs.directions:
                    nx, ny , ndir = self.dirs.move_from(x, y, d)
                    if 0 <= nx < rows and 0 <= ny < cols \
                        and (nx, ny, ndir) not in visited \
                        and self.rows[nx][ny] != self.dirs.wall:
                        queue.append((nx, ny, ndir, dist + 1))
                        visited.add((nx, ny, ndir))
                        if (nx, ny, d) not in parent:
                            parent[(nx, ny, ndir)] = (x, y, dir)
            return None , None

        self.start = self.grid.get_elem_pos('S')
        self.end = self.grid.get_elem_pos('E')
        self.start_dir = get_initial_dir(self.start[0], self.start[1])
        _ , path = shortest_path(self.start[0], self.start[1], self.start_dir)
        res = self.cheats_run(path, 2)
        return self.picos_below_limit(res, 100) , [path]

    def part2(self, args):
        res = self.cheats_run(args[0], 20)
        return self.picos_below_limit(res, 100)