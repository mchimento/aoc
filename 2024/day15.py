from day import Day
from directions import Directions
from grid import Grid
from itertools import groupby
from functools import reduce

class Day15(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        def scale_up():
            scaled_grid = []
            for row in self.rows:
                scaled_row = []
                for val in row:
                    if val == self.dirs.wall:
                        scaled_row += [self.dirs.wall, self.dirs.wall]
                    elif val == self.block:
                        scaled_row += ['[', ']']
                    elif val == self.empty:
                        scaled_row += ['.', '.']
                    else:
                        scaled_row += ['@', '.']
                scaled_grid.append(scaled_row)
            return scaled_grid

        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.dirs = Directions(self.rows, '#')
        self.grid = Grid(self.rows, self.dirs)
        self.block = 'O'
        self.empty = '.'
        self.wall = self.dirs.wall
        self.moves = self.input.rows_listed(self.input.process_data_as_rows(1))
        self.moves = reduce(lambda acc , xs : acc + xs, self.moves, [])
        self.scaled = scale_up()

    def get_block_coord(self, x , y , dir, exception = True):
        if dir == self.dirs.up:
            if x == 0 and exception:
                return x , y
            elif self.rows[x-1][y] == self.wall and exception:
                return x , y
            return x - 1 , y
        elif dir == self.dirs.down:
            if x == len(self.rows)-1 and exception:
                return x , y
            elif self.rows[x+1][y] == self.wall and exception:
                return x , y
            return x + 1 , y
        elif dir == self.dirs.left:
            if y == len(self.rows[0])-1 and exception:
                return x , y
            elif self.rows[x][y-1] == self.wall and exception:
                return x , y
            return x , y - 1
        elif dir == self.dirs.right:
            if y == 0 and exception:
                return x , y
            if self.rows[x][y+1] == self.wall and exception:
                return x , y
            return x , y + 1
        else:
            return None

    def get_expanded_blocks(self, xl , yl , xr , yr, dir):
        x  , _ = self.get_block_coord(xl, yl , dir, False)
        if x == 0 and dir == self.dirs.up:
            return []
        elif yl == 2 and self.rows[x][yl] != '[':
            return []
        elif yr == len(self.rows[0])-2 and self.rows[x][yr] != ']':
            return []
        elif x == len(self.rows)-1 and dir == self.dirs.down:
            return []
        elif yl == 2 and dir == self.dirs.down and self.rows[x][yl] != '[':
            return []
        elif self.rows[x][yl] != '[' \
            and self.rows[x][yl] != ']' \
            and self.rows[x][yr] != ']' \
            and self.rows[x][yr] != '[':
            return []
        blocks = []
        rec = []
        if self.rows[x][yl] == '[':
            blocks.append([(x, yl), (x, yr)])
        if self.rows[x][yl] == ']':
            blocks.append([(x, yl-1), (x, yl)])
        if self.rows[x][yr] == '[':
            blocks.append([(x, yr), (x, yr+1)])
        for b in blocks:
            rec += self.get_expanded_blocks(b[0][0], b[0][1], b[1][0], b[1][1], dir)
        return blocks + rec

    def touches_block(self, x , y, dir):
        if dir == self.dirs.up:
            return self.rows[x-1][y] == ']' \
                    or self.rows[x-1][y] == '['
        elif dir == self.dirs.down:
            return self.rows[x+1][y] == ']' \
                    or self.rows[x+1][y] == '['
        else:
            return False

    def block_can_be_shifted(self, xl , yl, xr, yr, xs, dir):
        if dir == self.dirs.up:
            if self.rows[xl-1][yl] == self.empty and self.rows[xr-1][yr] == self.empty:
                return True
            elif self.touches_block(xl, yl, dir) and self.rows[xr-1][yr] == self.empty:
                return True
            elif self.rows[xl-1][yl] == self.empty and self.touches_block(xr, yr, dir):
                return True
            elif self.touches_block(xl, yl, dir) and self.touches_block(xr, yr, dir):
                return True
            else:
                return False
        elif dir == self.dirs.down:
            if self.rows[xl+1][yl] == self.empty and self.rows[xr+1][yr] == self.empty:
                return True
            elif self.touches_block(xl, yl, dir) and self.rows[xr+1][yr] == self.empty:
                return True
            elif self.rows[xl+1][yl] == self.empty and self.touches_block(xr, yr, dir):
                return True
            elif self.touches_block(xl, yl, dir) and self.touches_block(xr, yr, dir):
                return True
            else:
                return False

    def shift_expanded_boxes(self, xi, yi, dir):
        if dir == self.dirs.up or dir == self.dirs.down:
            root = []
            if self.rows[xi][yi] == '[':
                root = [(xi, yi), (xi, yi+1)]
            elif self.rows[xi][yi] == ']':
                root = [(xi, yi-1), (xi, yi)]

            if not root:
                return False
            else:
                xl , yl , xr , yr = root[0][0], root[0][1], root[1][0], root[1][1]
                ex_blocks = self.get_expanded_blocks(xl , yl , xr , yr, dir)
                ex_blocks.append(root)
                if dir == self.dirs.up:
                    sorted_data = sorted(ex_blocks, key=lambda xs: xs[0][0])
                else:
                    sorted_data = sorted(ex_blocks, key=lambda xs: xs[0][0], reverse=True)
                nodes = [key for key, _ in groupby(sorted_data)]
                can_be_shifted = True
                for node in nodes:
                    xl , yl , xr , yr = node[0][0], node[0][1], node[1][0], node[1][1]
                    can_be_shifted = can_be_shifted and self.block_can_be_shifted(xl , yl , xr , yr, ex_blocks, dir)
                if can_be_shifted:
                    for node in nodes:
                        xl , yl , xr , yr = node[0][0], node[0][1], node[1][0], node[1][1]
                        xl_n , _ = self.get_block_coord(xl, yl, dir)
                        xr_n , _ =  self.get_block_coord(xr, yr, dir)
                        self.grid.swap(xl, yl, xl_n, yl, self.rows)
                        self.grid.swap(xr, yr, xr_n, yr, self.rows)
                return can_be_shifted
        elif dir == self.dirs.left:
            blocks = 0
            for i in range(yi, 0, -2):
                if self.rows[xi][i] == ']':
                    blocks += 1
                if self.rows[xi][i] == self.empty:
                    break
                if self.rows[xi][i] == self.dirs.wall:
                    return False
            blocks *= 2
            if yi - blocks <= 0:
                return False
            else:
                for i in range(yi-blocks, yi):
                    self.grid.swap(xi, i, xi, i+1, self.rows)
                return True
        elif dir == self.dirs.right:
            blocks = 0
            for i in range(yi, len(self.rows[0]), +2):
                if self.rows[xi][i] == '[':
                    blocks += 1
                if self.rows[xi][i] == self.empty:
                    break
                if self.rows[xi][i] == self.dirs.wall:
                    return False
            blocks *= 2
            if yi + blocks >= len(self.rows[0])-1:
                return False
            else:
                for i in range(yi+blocks, yi, -1):
                    self.grid.swap(xi, i, xi, i-1, self.rows)
                return True

    def shift_boxes(self, xi, yi, dir):
        if dir == self.dirs.up:
            blocks = 0
            for i in range(xi, 0, -1):
                if self.rows[i][yi] == self.block:
                    blocks += 1
                if self.rows[i][yi] == self.empty:
                    break
                if self.rows[i][yi] == self.dirs.wall:
                    return False
            if xi - blocks <= 0:
                return False
            else:
                for i in range(xi-blocks, xi):
                    self.grid.swap(i, yi, i+1, yi, self.rows)
                return True
        elif dir == self.dirs.down:
            blocks = 0
            for i in range(xi, len(self.rows)):
                if self.rows[i][yi] == self.block:
                    blocks += 1
                if self.rows[i][yi] == self.empty:
                    break
                if self.rows[i][yi] == self.dirs.wall:
                    return False
            if xi + blocks >= len(self.rows)-1:
                return False
            else:
                for i in range(xi+blocks, xi, -1):
                    self.grid.swap(i, yi, i-1, yi, self.rows)
                return True
        elif dir == self.dirs.left:
            blocks = 0
            for i in range(yi, 0, -1):
                if self.rows[xi][i] == self.block:
                    blocks += 1
                if self.rows[xi][i] == self.empty:
                    break
                if self.rows[xi][i] == self.dirs.wall:
                    return False
            if yi - blocks <= 0:
                return False
            else:
                for i in range(yi-blocks, yi):
                    self.grid.swap(xi, i, xi, i+1, self.rows)
                return True
        elif dir == self.dirs.right:
            blocks = 0
            for i in range(yi, len(self.rows[0])):
                if self.rows[xi][i] == self.block:
                    blocks += 1
                if self.rows[xi][i] == self.empty:
                    break
                if self.rows[xi][i] == self.dirs.wall:
                    return False
            if yi + blocks >= len(self.rows[0])-1:
                return False
            else:
                for i in range(yi+blocks, yi, -1):
                    self.grid.swap(xi, i, xi, i-1, self.rows)
                return True

    def is_block_scaled(self, xi, yi, dir):
        if dir == self.dirs.up or dir == self.dirs.down:
            return self.rows[xi][yi-1] == '[' and self.rows[xi][yi] == ']' \
                    or self.rows[xi][yi] == '[' and self.rows[xi][yi+1] == ']'
        elif dir == self.dirs.left:
            return self.rows[xi][yi] == ']'
        elif dir == self.dirs.right:
            return self.rows[xi][yi] == '['

    def take_step(self, dir, is_scaled = False):
        if is_scaled:
            xi, yi = self.get_block_coord(self.x, self.y ,dir)
        else:
            xi, yi , _ = self.dirs.move_from(self.x, self.y, dir)
        if not is_scaled and self.rows[xi][yi] == self.block:
            if self.shift_boxes(xi, yi, dir):
                self.grid.swap(self.x, self.y, xi, yi, self.rows)
                self.x , self.y = xi , yi
        elif self.is_block_scaled(xi, yi, dir):
            if self.shift_expanded_boxes(xi, yi, dir):
                self.grid.swap(self.x, self.y, xi, yi, self.rows)
                self.x , self.y = xi , yi
        else:
            self.grid.swap(self.x, self.y, xi, yi, self.rows)
            self.x , self.y = xi , yi

    def part1(self):
        def gps():
            res = 0
            for xi in range(0, len(self.rows)):
                for yi in range(0, len(self.rows[0])):
                    if self.rows[xi][yi] == self.block:
                        res += (100 * xi) + yi
            return res

        self.x , self.y = self.grid.get_elem_pos('@')
        for move in self.moves:
            self.take_step(move)
        return gps()

    def part2(self):
        def scaled_gps():
            res = 0
            for xi in range(0, len(self.rows)):
                for yi in range(0, len(self.rows[0])):
                    if self.rows[xi][yi] == '[':
                        res += (100 * xi) + yi
            return res

        self.x , self.y = self.grid.get_elem_pos('@', self.scaled)
        self.rows = self.scaled
        for move in self.moves:
            self.take_step(move, True)
        return scaled_gps()