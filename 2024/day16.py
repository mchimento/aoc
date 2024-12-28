from day import Day
from directions import Directions
from grid import Grid
import heapq

class Day16(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.dirs = Directions(self.rows, '#')
        self.grid = Grid(self.rows, self.dirs)

    def part1(self):
        def shortest_paths():
            pq = []
            parent = {}
            heapq.heappush(pq, (0, start[0], start[1], self.dirs.right))  # (cost, x, y, dir)
            visited = set()

            while pq:
                cost, x, y, dir = heapq.heappop(pq)
                if self.rows[x][y] == end:
                    all_paths = []
                    reconstruct_paths(x, y, dir, parent, all_paths, [(start[0], start[1])])
                    all_paths.reverse()
                    return cost, all_paths

                if (x, y, dir) in visited:
                    continue
                visited.add((x, y, dir))

                nx , ny, ndir = self.dirs.move_from(x , y, dir)
                if dir == ndir:
                    if (nx, ny, dir) not in visited:
                        heapq.heappush(pq, (cost + 1, nx, ny, dir))
                        if (nx, ny, dir) not in parent:
                            parent[(nx, ny, dir)] = []
                        parent[(nx, ny, dir)].append((x, y, dir))
                for turn, new_dir in [(1000, self.dirs.rotate90_clockwise(dir)), (1000, self.dirs.rotate90_anticlockwise(dir))]:
                    if (x, y, new_dir) not in visited:
                        heapq.heappush(pq, (cost + turn, x, y, new_dir))
                        if (x, y, new_dir) not in parent:
                            parent[(x, y, new_dir)] = []
                        parent[(x, y, new_dir)].append((x, y, dir))

            return None, []

        def reconstruct_paths(x, y, dir, parent, all_paths, current_path):
            if (x, y, dir) == (start[0], start[1], self.dirs.right):
                all_paths.append(list(current_path))
                return
            if (x, y, dir) in parent:
                for px, py, pdir in parent[(x, y, dir)]:
                    current_path.append((px, py))
                    reconstruct_paths(px, py, pdir, parent, all_paths, current_path)
                    current_path.pop()

        start = self.grid.get_elem_pos('S')
        end = 'E'
        points , paths = shortest_paths()
        return points , [paths]

    def part2(self, args):
        def count_tiles(paths):
            tiles = set()
            for path in paths:
                for node in path:
                    tiles.add(node)
                    self.rows[node[0]][node[1]] = 'O'
            return len(tiles)+1
        return count_tiles(args[0])