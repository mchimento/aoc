import heapq
from directions import Directions
import numpy as np

class Grid:

    def __init__(self, grid = None, dirs : Directions =None):
        self.grid = np.array(grid) if grid is not None else None
        self.dirs= dirs if dirs is not None else Directions()

    def __getitem__(self, index):
        return str(self.grid[index])

    def __setitem__(self, index, value):
        self.grid[index] = value

    def get_elem_pos(self, elem, grid_arg=None):
        grid = grid_arg if grid_arg is not None else self.grid
        pos = np.where(grid == elem)
        positions = tuple((int(x), int(y)) for x, y in zip(pos[0], pos[1]))

        return positions[0] if len(positions) == 1 else positions

    def get(self, x, y, grid_arg=None):
        grid = grid_arg if grid_arg is not None else self.grid
        return str(grid[x, y])

    def is_valid_coord(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def height(self, arg_grid=None):
        return len(self.grid) if arg_grid is None else len(arg_grid)

    def width(self, arg_grid=None):
        return len(self.grid[0]) if arg_grid is None else len(arg_grid[0])

    def create_empty(self, height, width, value='.'):
        self.grid = np.full((height, width), value)

    def swap(self, x, y, xi, yi, grid=None):
        if grid is not None:
            grid[x, y], grid[xi, yi] = grid[xi, yi], grid[x, y]
        else:
            self.grid[x, y], self.grid[xi, yi] = self.grid[xi, yi], self.grid[x, y]

    def fill_grid(self, positions, elem):
        if positions is None:
            return
        for i, j in positions:
            self.grid[i, j] = elem

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

    def transpose(self, grid=None):
        if grid is not None:
            to_tr = grid
        return [''.join(column) for column in zip(*to_tr)]

    def reachable_nodes(self, x, y, max_dist=1, height=None, width=None):
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

    def get_adjacent(self, x, y, include_diagonals=True, height=None, width=None, filter_func=None):
        """
        Get all adjacent positions to (x, y) in the grid.
        
        Args:
            x, y: Coordinates of the position
            include_diagonals: If True, includes diagonal adjacent positions (8-way).
                            If False, only includes horizontal/vertical positions (4-way).
            height, width: Optional grid dimensions. If not provided, uses the grid's dimensions.
            filter_func: Optional function that takes (x, y) and returns True if the position should be included.
        
        Returns:
            List of (x, y) tuples representing adjacent positions.
        """
        adjacent = []
        if height is None:
            height, width = len(self.grid), len(self.grid[0])
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if not include_diagonals and dx != 0 and dy != 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width:
                    if filter_func is None or filter_func(nx, ny):
                        adjacent.append((nx, ny))
        
        return adjacent

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

    def move_from(self, x , y, dir):
        """
        Move from position (x, y) in grid one step in the direction dir,
        unless the step is blocked by wall or we are the grid border
        """
        if dir == self.dirs.up:
            if x == 0:
                return x , y , self.dirs.rotate90_clockwise(dir)
            if self.dirs.wall is not None and self.grid[x-1, y] == self.dirs.wall:
                return x , y, self.dirs.rotate90_clockwise(dir)
            else:
                return x-1 , y, dir
        elif dir == self.dirs.down:
            if x == len(self.grid)-1:
                return x , y, self.dirs.rotate90_clockwise(dir)
            if self.dirs.wall is not None and self.grid[x+1, y] == self.dirs.wall:
                return x , y, self.dirs.rotate90_clockwise(dir)
            else:
                return x+1 , y , dir
        elif dir == self.dirs.right:
            if y == len(self.grid[0])-1:
                return x , y, self.dirs.rotate90_clockwise(dir)
            if self.dirs.wall is not None and self.grid[x, y+1] == self.dirs.wall:
                return x , y, self.dirs.rotate90_clockwise(dir)
            else:
                return x , y+1, dir
        elif dir == self.dirs.left:
            if y == 0:
                return x , y, self.dirs.rotate90_clockwise(dir)
            if self.dirs.wall is not None and self.grid[x, y-1] == self.dirs.wall:
                return x , y, self.dirs.rotate90_clockwise(dir)
            else:
                return x , y-1, dir
        else:
            return None

    def find_enclosed_nodes_within_closed_path(self, path, grid_arg=None, empty='.'):
        """
        Find all nodes enclosed by a given closed path.
        """
        if grid_arg is None:
            grid = self.grid
        else:
            grid = grid_arg
        def is_point_inside_path(x, y, path):
            """
            Check if a point (x, y) is inside a polygon, i.e. path, using the Ray-Casting Algorithm.
            """
            n = len(path)
            inside = False

            for i in range(n):
                x1, y1 = path[i]
                x2, y2 = path[(i + 1) % n]

                # Check if point is on the boundary
                if (y == y1 == y2 and min(x1, x2) <= x <= max(x1, x2)) or \
                    (x == x1 == x2 and min(y1, y2) <= y <= max(y1, y2)):
                    return False  # Treat points on the boundary as outside

                # Check if ray crosses the edge
                if (y > min(y1, y2)) and (y <= max(y1, y2)) and (x <= max(x1, x2)):
                    if y1 != y2:  # Avoid division by zero
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or x <= xinters:
                        inside = not inside

            return inside

        enclosed_nodes = []

        for x in range(self.height(grid)):
            for y in range(self.width(grid)):
                if (x, y) in path:
                    continue
                if grid[x, y] == empty:
                    if is_point_inside_path(x, y, path):
                        enclosed_nodes.append((x, y))
        return enclosed_nodes

    def shortest_paths_rot(self, start, end, start_dir, grid_arg=None, dirs_arg=None):
        """
        Shortest path algorithm including directations and rotations
        """
        pq = []
        parent = {}
        heapq.heappush(pq, (0, start[0], start[1], start_dir))  # (cost, x, y, dir)
        visited = set()

        if grid_arg is not None:
            grid = grid_arg
            dirs = dirs_arg
        else:
            grid = self.grid
            dirs = self.dirs

        while pq:
            cost, x, y, dir = heapq.heappop(pq)
            if grid[x, y] == end:
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

    def shortest_paths(self, start, end, grid_arg=None, dirs_arg=None):
        """
        General shortest path algorithm
        """
        pq = []
        parent = {}
        heapq.heappush(pq, (0, start[0], start[1]))  # (cost, x, y)
        visited = set()
        if grid_arg is not None:
            grid = grid_arg
            dirs = dirs_arg
        else:
            grid = self.grid
            dirs = self.dirs

        rows , cols = len(grid)-1 , len(grid[0])-1

        while pq:
            cost, x, y = heapq.heappop(pq)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if grid[x, y] == end:
                all_paths = []
                self.reconstruct_paths(x, y, start, parent, all_paths, [(x, y)])
                all_paths = list(map(lambda xs: xs[::-1], all_paths))
                return cost, all_paths

            for d in dirs.directions:
                dx , dy = dirs.coord(d)
                nx, ny = x + dx , y + dy
                if 0 <= nx <= rows and 0 <= ny <= cols \
                    and (nx, ny) not in visited \
                    and grid[nx, ny] != dirs.wall:
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