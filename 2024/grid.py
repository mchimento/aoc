from directions import Directions
import heapq

class Coordinate:

    def __init__(self):
        self.x = None
        self.y = None
        self.dir = None

class Grid:

    def __init__(self, grid = None, dirs=None):
        self.grid = grid
        self.dirs= dir

    def get_elem_pos(self, elem):
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                if self.grid[x][y] == elem:
                    return (x, y)
        return None

    def print_grid(self, grid=None):
        to_print = self.grid
        if grid is not None:
            to_print = grid
        for row in to_print:
            print(row)

    def pretty_print_grid(self, grid=None):
        to_print = self.grid
        if grid is not None:
            to_print = grid
        for row in to_print:
            print(''.join(row))

    def shortest_paths_rot(self, start, end, start_dir, grid, dirs):
        """
        Shortest path algorithm including directations and rotations
        """
        pq = []
        parent = {}
        heapq.heappush(pq, (0, start[0], start[1], start_dir))  # (cost, x, y, dir)
        visited = set()

        while pq:
            cost, x, y, dir = heapq.heappop(pq)
            if grid[x][y] == end:
                all_paths = []
                self.reconstruct_paths_dir(x, y, dir, start, start_dir, parent, all_paths, [(x, y, dir)])
                all_paths = list(map(lambda xs: xs[::-1], all_paths))
                return cost, all_paths

            if (x, y, dir) in visited:
                continue
            visited.add((x, y, dir))

            nx , ny, ndir = dirs.move_from(x , y, dir)
            if dir == ndir:
                if (nx, ny, ndir) not in visited:
                    heapq.heappush(pq, (cost + 1, nx, ny, ndir))
                    if (nx, ny, ndir) not in parent:
                        parent[(nx, ny, ndir)] = []
                    parent[(nx, ny, ndir)].append((x, y, ndir))
            for new_dir in [dirs.rotate90_clockwise(dir), dirs.rotate90_anticlockwise(dir)]:
                if (x, y, new_dir) not in visited:
                    heapq.heappush(pq, (cost + 1, x, y, new_dir))
                    if (x, y, new_dir) not in parent:
                        parent[(x, y, new_dir)] = []
                    parent[(x, y, new_dir)].append((x, y, dir))

        return None, []

    def reconstruct_paths_dir(self, x, y, dir, start, start_dir, parent, all_paths, current_path):
        if (x, y, dir) == (start[0], start[1], start_dir):
            all_paths.append(list(current_path))
            return
        if (x, y, dir) in parent:
            for px, py, pdir in parent[(x, y, dir)]:
                current_path.append((px, py, pdir))
                self.reconstruct_paths_dir(px, py, pdir, start, start_dir, parent, all_paths, current_path)
                current_path.pop()

    def shortest_paths(self, start, end, grid, dirs):
        """
        Shortest path algorithm
        """
        pq = []
        parent = {}
        heapq.heappush(pq, (0, start[0], start[1]))  # (cost, x, y)
        visited = set()
        rows , cols = len(grid)-1 , len(grid[0])-1

        while pq:
            cost, x, y = heapq.heappop(pq)
            if grid[x][y] == end:
                all_paths = []
                self.reconstruct_paths(x, y, start, parent, all_paths, [(x, y)])
                all_paths = list(map(lambda xs: xs[::-1], all_paths))
                return cost, all_paths

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for d in dirs.directions:
                dx , dy = dirs.coord(d)
                nx, ny = x + dx , y + dy
                if 0 <= nx <= rows and 0 <= ny <= cols \
                    and (nx, ny) not in visited \
                    and grid[nx][ny] != dirs.wall:
                    heapq.heappush(pq, (cost + 1, nx, ny))
                    if (nx, ny) not in parent:
                        parent[(nx, ny)] = []
                    parent[(nx, ny)].append((x, y))

        return None, []

    def reconstruct_paths(self, x, y, start, parent, all_paths, current_path):
        if (x, y) == (start[0], start[1]):
            all_paths.append(list(current_path))
            return
        if (x, y) in parent:
            for px, py in parent[(x, y)]:
                current_path.append((px, py))
                self.reconstruct_paths(px, py, start, parent, all_paths, current_path)
                current_path.pop()