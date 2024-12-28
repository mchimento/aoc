from day import Day
from directions import Directions
from grid import Grid

class Day06(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.dirs = Directions(self.rows, '#')
        self.grid = Grid(self.rows, self.dirs)

    def find_path(self, start, dir, obs=None):
        x, y = start
        visited = set()
        pos_vectors = set()
        pos_vectors.add((x, y, dir))

        def is_inbounds(x, y):
            return 0 <= x < len(self.rows) and 0 <= y < len(self.rows[0])

        while is_inbounds(x, y):
            visited.add((x, y))
            dx, dy = self.dirs.coord(dir)
            nx, ny = x + dx, y + dy

            if is_inbounds(nx, ny) and (self.rows[nx][ny] == self.dirs.wall or (obs and (nx, ny) == obs)):
                dir = self.dirs.rotate90_clockwise(dir)
            else:
                x, y = nx, ny

            pos_vector = (x, y, dir)
            if pos_vector in pos_vectors:
                return True, visited
            pos_vectors.add(pos_vector)

        return False, visited

    def part1(self):
        start = self.grid.get_elem_pos(self.dirs.up)
        _, visited = self.find_path(start, self.dirs.up)
        return len(visited) , [start , visited]

    def part2(self , args):
        result = 0
        start , visited = args[0] , args[1]
        obstacles = visited - {start}
        for obs in obstacles:
            if self.find_path(start, self.dirs.up, obs)[0]:
                result += 1
        return result