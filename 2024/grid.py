import heapq

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

    def create_empty(self, height, width):
        self.grid = [["."] * width for _ in range(height)]

    def fill_grid(self, positions, elem):
        if positions is None:
            return
        for i, j in positions:
            self.grid[i][j] = elem

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

    def reachable_nodes(self, x, y, max_dist, height=None, width=None):
            reachable = []
            if height is None:
                height , width = len(self.grid) , len(self.grid[0])
            for dx in range(-max_dist, max_dist + 1):
                remaining_dist = max_dist - abs(dx)
                for dy in range(-remaining_dist, remaining_dist + 1):
                    if dx == dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < height and 0 <= ny < width:
                        reachable.append((nx, ny))
            return reachable

    def manhattan_distance(self, point1, point2):
        """
        Calculate the Manhattan distance between two points,
        i.e. distance between two points in a grid-based system
        moving only horizontally and vertically.

        Parameters:
        - point1 (tuple): Coordinates of the first point (x1, y1).
        - point2 (tuple): Coordinates of the second point (x2, y2).
        """
        return sum(abs(a - b) for a, b in zip(point1, point2))

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
        General shortest path algorithm
        """
        pq = []
        parent = {}
        heapq.heappush(pq, (0, start[0], start[1]))  # (cost, x, y)
        visited = set()
        rows , cols = len(grid)-1 , len(grid[0])-1

        while pq:
            cost, x, y = heapq.heappop(pq)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if grid[x][y] == end:
                all_paths = []
                self.reconstruct_paths(x, y, start, parent, all_paths, [(x, y)])
                all_paths = list(map(lambda xs: xs[::-1], all_paths))
                return cost, all_paths

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