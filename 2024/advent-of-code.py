import re
from itertools import groupby
from collections import deque , defaultdict
import heapq
from directions import Directions
from grid import Grid
import time
from functools import reduce
from day14 import Day14
from day import Day

class AdventOfCode:

    def get_initial_pos(self, elem):
        for x in range(0, len(self.rows)):
            for y in range(0, len(self.rows[0])):
                if self.rows[x][y] == elem:
                    return (x, y)
        return None

    def print_to_file(self, s, file_path="output.txt", type='a'):
        with open(file_path, type) as file:
            print(s, file=file)

    def split_str_by_fun(self, grid, fun):
        grid = [ fun(row) for row in grid ]
        return grid

    def is_valid(self, x , y):
        return 0 <= x < len(self.rows) \
               and 0 <= y < len(self.rows[0])

    def swap(self, x, y, xs):
        xs[x], xs[y] = xs[y], xs[x]

    def swap_grid(self, x, y, xi, yi, grid):
        grid[x][y], grid[xi][yi] = grid[xi][yi], grid[x][y]

    def default(self, val, default):
        if val is None:
            return default
        else:
            return val

    def print_rows(self, rows):
        for row in rows:
            print(row)

    def pretty_print_rows(self, rows):
        for row in rows:
            print(''.join(row))

    def make_grid_str(self, grid):
        aux = ""
        for row in grid:
            aux += ''.join(row) + "\n"
        return aux

    def day15(self):
        dirs = Directions(self.rows, '#')
        block = 'O'
        empty = '.'
        wall = '#'
        self.x , self.y = self.get_initial_pos('@')
        def get_block_coord(x , y , dir, exception = True):
            if dir == dirs.up:
                if x == 0 and exception:
                    return x , y
                elif self.rows[x-1][y] == wall and exception:
                    return x , y
                return x - 1 , y
            elif dir == dirs.down:
                if x == len(self.rows)-1 and exception:
                    return x , y
                elif self.rows[x+1][y] == wall and exception:
                    return x , y
                return x + 1 , y
            elif dir == dirs.left:
                if y == len(self.rows[0])-1 and exception:
                    return x , y
                elif self.rows[x][y-1] == wall and exception:
                    return x , y
                return x , y - 1
            elif dir == dirs.right:
                if y == 0 and exception:
                    return x , y
                if self.rows[x][y+1] == wall and exception:
                    return x , y
                return x , y + 1
            else:
                return None

        def get_expanded_blocks(xl , yl , xr , yr, dir):
            x  , _ = get_block_coord(xl, yl , dir, False)
            if x == 0 and dir == dirs.up:
                return []
            elif yl == 2 and self.rows[x][yl] != '[':
                return []
            elif yr == len(self.rows[0])-2 and self.rows[x][yr] != ']':
                return []
            elif x == len(self.rows)-1 and dir == dirs.down:
                return []
            elif yl == 2 and dir == dirs.down and self.rows[x][yl] != '[':
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
                rec += get_expanded_blocks(b[0][0], b[0][1], b[1][0], b[1][1], dir)
            return blocks + rec

        def touches_block(x , y, dir):
            if dir == dirs.up:
                return self.rows[x-1][y] == ']' \
                       or self.rows[x-1][y] == '['
            elif dir == dirs.down:
                return self.rows[x+1][y] == ']' \
                       or self.rows[x+1][y] == '['
            else:
                return False

        def block_can_be_shifted(xl , yl, xr, yr, xs, dir):
            if dir == dirs.up:
                if self.rows[xl-1][yl] == empty and self.rows[xr-1][yr] == empty:
                    return True
                elif touches_block(xl, yl, dir) and self.rows[xr-1][yr] == empty:
                    return True
                elif self.rows[xl-1][yl] == empty and touches_block(xr, yr, dir):
                    return True
                elif touches_block(xl, yl, dir) and touches_block(xr, yr, dir):
                    return True
                else:
                    return False
            elif dir == dirs.down:
                if self.rows[xl+1][yl] == empty and self.rows[xr+1][yr] == empty:
                    return True
                elif touches_block(xl, yl, dir) and self.rows[xr+1][yr] == empty:
                    return True
                elif self.rows[xl+1][yl] == empty and touches_block(xr, yr, dir):
                    return True
                elif touches_block(xl, yl, dir) and touches_block(xr, yr, dir):
                    return True
                else:
                    return False

        def shift_expanded_boxes(xi, yi, dir):
            if dir == dirs.up or dir == dirs.down:
                root = []
                if self.rows[xi][yi] == '[':
                    root = [(xi, yi), (xi, yi+1)]
                elif self.rows[xi][yi] == ']':
                    root = [(xi, yi-1), (xi, yi)]

                if not root:
                    return False
                else:
                    xl , yl , xr , yr = root[0][0], root[0][1], root[1][0], root[1][1]
                    ex_blocks = get_expanded_blocks(xl , yl , xr , yr, dir)
                    ex_blocks.append(root)
                    if dir == dirs.up:
                        sorted_data = sorted(ex_blocks, key=lambda xs: xs[0][0])
                    else:
                        sorted_data = sorted(ex_blocks, key=lambda xs: xs[0][0], reverse=True)
                    nodes = [key for key, _ in groupby(sorted_data)]
                    can_be_shifted = True
                    for node in nodes:
                        xl , yl , xr , yr = node[0][0], node[0][1], node[1][0], node[1][1]
                        can_be_shifted = can_be_shifted and block_can_be_shifted(xl , yl , xr , yr, ex_blocks, dir)
                    if can_be_shifted:
                        for node in nodes:
                            xl , yl , xr , yr = node[0][0], node[0][1], node[1][0], node[1][1]
                            xl_n , _ = get_block_coord(xl, yl, dir)
                            xr_n , _ =  get_block_coord(xr, yr, dir)
                            self.swap_grid(xl, yl, xl_n, yl, self.rows)
                            self.swap_grid(xr, yr, xr_n, yr, self.rows)
                    return can_be_shifted
            elif dir == dirs.left:
                blocks = 0
                for i in range(yi, 0, -2):
                    if self.rows[xi][i] == ']':
                        blocks += 1
                    if self.rows[xi][i] == empty:
                        break
                    if self.rows[xi][i] == dirs.wall:
                        return False
                blocks *= 2
                if yi - blocks <= 0:
                    return False
                else:
                    for i in range(yi-blocks, yi):
                        self.swap_grid(xi, i, xi, i+1, self.rows)
                    return True
            elif dir == dirs.right:
                blocks = 0
                for i in range(yi, len(self.rows[0]), +2):
                    if self.rows[xi][i] == '[':
                        blocks += 1
                    if self.rows[xi][i] == empty:
                        break
                    if self.rows[xi][i] == dirs.wall:
                        return False
                blocks *= 2
                if yi + blocks >= len(self.rows[0])-1:
                    return False
                else:
                    for i in range(yi+blocks, yi, -1):
                        self.swap_grid(xi, i, xi, i-1, self.rows)
                    return True

        def shift_boxes(xi, yi, dir):
            if dir == dirs.up:
                blocks = 0
                for i in range(xi, 0, -1):
                    if self.rows[i][yi] == block:
                        blocks += 1
                    if self.rows[i][yi] == empty:
                        break
                    if self.rows[i][yi] == dirs.wall:
                        return False
                if xi - blocks <= 0:
                    return False
                else:
                    for i in range(xi-blocks, xi):
                        self.swap_grid(i, yi, i+1, yi, self.rows)
                    return True
            elif dir == dirs.down:
                blocks = 0
                for i in range(xi, len(self.rows)):
                    if self.rows[i][yi] == block:
                        blocks += 1
                    if self.rows[i][yi] == empty:
                        break
                    if self.rows[i][yi] == dirs.wall:
                        return False
                if xi + blocks >= len(self.rows)-1:
                    return False
                else:
                    for i in range(xi+blocks, xi, -1):
                        self.swap_grid(i, yi, i-1, yi, self.rows)
                    return True
            elif dir == dirs.left:
                blocks = 0
                for i in range(yi, 0, -1):
                    if self.rows[xi][i] == block:
                        blocks += 1
                    if self.rows[xi][i] == empty:
                        break
                    if self.rows[xi][i] == dirs.wall:
                        return False
                if yi - blocks <= 0:
                    return False
                else:
                    for i in range(yi-blocks, yi):
                        self.swap_grid(xi, i, xi, i+1, self.rows)
                    return True
            elif dir == dirs.right:
                blocks = 0
                for i in range(yi, len(self.rows[0])):
                    if self.rows[xi][i] == block:
                        blocks += 1
                    if self.rows[xi][i] == empty:
                        break
                    if self.rows[xi][i] == dirs.wall:
                        return False
                if yi + blocks >= len(self.rows[0])-1:
                    return False
                else:
                    for i in range(yi+blocks, yi, -1):
                        self.swap_grid(xi, i, xi, i-1, self.rows)
                    return True
        def is_block_scaled(xi, yi, dir):
            if dir == dirs.up or dir == dirs.down:
                return self.rows[xi][yi-1] == '[' and self.rows[xi][yi] == ']' \
                       or self.rows[xi][yi] == '[' and self.rows[xi][yi+1] == ']'
            elif dir == dirs.left:
                return self.rows[xi][yi] == ']'
            elif dir == dirs.right:
                return self.rows[xi][yi] == '['

        def take_step(dir, is_scaled = False):
            if is_scaled:
                xi, yi = get_block_coord(self.x, self.y ,dir)
                with open("output.txt", "a") as file:
                    # Write the input to the file
                    str = f"from ({self.x , self.y})"
                    file.write(f"{str} move to {xi , yi} in direction {dir}\n")
            else:
                xi, yi , _ = dirs.move_from(self.x, self.y, dir)
            if not is_scaled and self.rows[xi][yi] == block:
                if shift_boxes(xi, yi, dir):
                    self.swap_grid(self.x, self.y, xi, yi, self.rows)
                    self.x , self.y = xi , yi
            elif is_block_scaled(xi, yi, dir):
                if shift_expanded_boxes(xi, yi, dir):
                    self.swap_grid(self.x, self.y, xi, yi, self.rows)
                    self.x , self.y = xi , yi
            else:
                self.swap_grid(self.x, self.y, xi, yi, self.rows)
                self.x , self.y = xi , yi
        def gps():
            res = 0
            for xi in range(0, len(self.rows)):
                for yi in range(0, len(self.rows[0])):
                    if self.rows[xi][yi] == block:
                        res += (100 * xi) + yi
            return res
        def scaled_gps():
            res = 0
            for xi in range(0, len(self.rows)):
                for yi in range(0, len(self.rows[0])):
                    if self.rows[xi][yi] == '[':
                        res += (100 * xi) + yi
            return res
        def scale_up():
            scaled_grid = []
            for row in self.rows:
                scaled_row = []
                for val in row:
                    if val == dirs.wall:
                        scaled_row += [dirs.wall,dirs.wall]
                    elif val == block:
                        scaled_row += ['[', ']']
                    elif val == empty:
                        scaled_row += ['.', '.']
                    else:
                        scaled_row += ['@', '.']
                scaled_grid.append(scaled_row)
            return scaled_grid

        scaled_rows = scale_up()
        for move in self.moves:
            take_step(move)
        print(f"Part 1: {gps()}")
        self.rows = scaled_rows
        self.x , self.y = self.get_initial_pos('@')
        for move in self.moves:
            take_step(move, True)
        print(f"Part 2: {scaled_gps()}")

    def day16(self):
        dirs = Directions(self.rows, wall="#")
        start = self.get_initial_pos('S')
        end = 'E'
        def parse_input():
            self.rows = [ list(row) for row in self.rows ]

        def shortest_paths():
            pq = []
            parent = {}
            heapq.heappush(pq, (0, start[0], start[1], dirs.right))  # (cost, x, y, dir)
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

                nx , ny, ndir = dirs.move_from(x , y, dir)
                if dir == ndir:
                    if (nx, ny, dir) not in visited:
                        heapq.heappush(pq, (cost + 1, nx, ny, dir))
                        if (nx, ny, dir) not in parent:
                            parent[(nx, ny, dir)] = []
                        parent[(nx, ny, dir)].append((x, y, dir))
                for turn, new_dir in [(1000, dirs.rotate90_clockwise(dir)), (1000, dirs.rotate90_anticlockwise(dir))]:
                    if (x, y, new_dir) not in visited:
                        heapq.heappush(pq, (cost + turn, x, y, new_dir))
                        if (x, y, new_dir) not in parent:
                            parent[(x, y, new_dir)] = []
                        parent[(x, y, new_dir)].append((x, y, dir))

            return None, []

        def reconstruct_paths(x, y, dir, parent, all_paths, current_path):
            if (x, y, dir) == (start[0], start[1], dirs.right):
                all_paths.append(list(current_path))
                return
            if (x, y, dir) in parent:
                for px, py, pdir in parent[(x, y, dir)]:
                    current_path.append((px, py))
                    reconstruct_paths(px, py, pdir, parent, all_paths, current_path)
                    current_path.pop()

        def count_tiles(paths):
            tiles = set()
            for path in paths:
                for node in path:
                    tiles.add(node)
                    self.rows[node[0]][node[1]] = 'O'
            return len(tiles)+1

        parse_input()
        points , paths = shortest_paths()
        print(f"Part 1: {points}")
        print(f"Part 2: {count_tiles(paths)}")

    def day17(self):
        def parse_input():
            parsed = {}
            for row in self.rows:
                parse = row.replace('Register', '').strip().split(':')
                key , val = parse[0] , parse[1]
                parsed[key] = int(val)
            self.rows = parsed
            self.program = self.int_list(self.program[0].replace('Program:', '').strip().split(','))
        def literal_val(literal):
            return literal
        def combo_val(combo):
            if 0 <= combo <= 3:
                return combo
            elif combo == 4:
                return self.rows['A']
            elif combo == 5:
                return self.rows['B']
            elif combo == 6:
                return self.rows['C']
            else:
                return None
        def eval(opcode, operand):
            match opcode:
                case 0:
                    numerator = self.rows['A']
                    denominator = 2 ** combo_val(operand)
                    self.rows['A'] = numerator // denominator
                    self.pointer += 2
                case 1:
                    self.rows['B'] = self.rows['B'] ^ literal_val(operand)
                    self.pointer += 2
                case 2:
                    self.rows['B'] = combo_val(operand) % 8
                    self.pointer += 2
                case 3:
                    if self.rows['A'] == 0:
                        self.pointer += 2
                    else:
                        self.pointer = literal_val(operand)
                case 4:
                    self.rows['B'] = self.rows['B'] ^ self.rows['C']
                    self.pointer += 2
                case 5:
                    val = combo_val(operand) % 8
                    self.pointer += 2
                    return str(val)
                case 6:
                    numerator = self.rows['A']
                    denominator = 2 ** combo_val(operand)
                    self.rows['B'] = numerator // denominator
                    self.pointer += 2
                case 7:
                    numerator = self.rows['A']
                    denominator = 2 ** combo_val(operand)
                    self.rows['C'] = numerator // denominator
                    self.pointer += 2
            return ""

        def eval_program():
            if self.pointer == len(self.program)-1:
                print("halt")
            ret = eval(self.program[self.pointer], self.program[self.pointer+1])
            if self.pointer == len(self.program):
                return ret
            else:
                return ret + eval_program()

        def reset_memory():
            self.rows['A'] = 0
            self.rows['B'] = 0
            self.rows['C'] = 0
            self.pointer = 0

        def eval_for(val):
            reset_memory()
            self.rows['A'] = val
            return self.int_list(eval_program())

        def get_min_A(A=0, ix=0):
            """
            while a != 0 {
                b = a % 8
                b = b ^ 2
                c = a // (2 ** b)
                b = b ^ 7
                b = b ^ c
                a = a // 8
                out(b % 8)
            }

            Program: 0,3,5,4,3,0
            while a != 0 {
                a = a // 8
                out(a % 8)
            }
            """
            # bitwise comparison based on the fact that in the input we have a // 8, and the program manipulates its (last) bits
            if ix == len(self.program):
                return A
            for i in range(8):
                ret = eval_for(A * 8 + i)
                if ret[0] == self.program[len(self.program) - 1 - ix]:
                    ret_val = get_min_A((A * 8 + i), ix + 1)
                    if ret_val:
                        return ret_val

        parse_input()
        self.pointer = 0
        print(f"Part 1: {",".join(list(eval_program()))}")
        print(f"Part 2: {get_min_A()}")

    def day18(self):
        self.grid = []
        dirs = Directions(self.grid, wall="#")
        def parse_input():
            parsed = []
            for row in self.rows:
                parse = self.int_list(row.split(','))
                parsed.append(parse)
            self.rows = parsed
        def create_grid(size):
            if self.grid:
                self.grid = []
            for _ in range(size):
                self.grid.append([ dirs.empty for i in range(size)])

        def shortest_path():
            rows, cols = len(self.grid), len(self.grid[0])
            visited = set()
            parent = {}
            queue = deque([(0, 0, 0, dirs.right)])  # (x, y, distance, dir)

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
                for d in dirs.directions:
                    nx, ny , ndir = dirs.move_from(x, y, d)
                    if (nx, ny, ndir) not in visited and self.grid[nx][ny] != dirs.wall:
                        queue.append((nx, ny, dist + 1, ndir))
                        visited.add((nx, ny, ndir))
                        if (nx, ny) not in parent:
                            parent[(nx, ny, ndir)] = (x, y, dir)
            return None , None

        def drop_byte(x , y):
            self.grid[y][x] = dirs.wall
        def drop_bytes(limit=None):
            i = 0
            for x , y in self.rows:
                if limit is not None and i==limit:
                    break
                i+=1
                drop_byte(x, y)

        def first_block():
            _ , path = shortest_path()
            while path is not None and self.rows:
                x , y = self.rows.pop(0)
                drop_byte(x,y)
                _ , path = shortest_path()
            return x , y

        parse_input()
        create_grid(71)
        drop_bytes(1024)
        dist , _ = shortest_path()
        print(f"Part 1: {dist}")
        create_grid(71)
        print(f"Part 2: {first_block()}")

    def day19(self):
        self.patterns = self.rows
        def parse_input():
            self.patterns = list(map(lambda x : x.strip(), self.patterns[0].split(",")))
        def get_valid_patterns(design):
            found = []
            for pattern in self.patterns:
                founded = re.search(pattern, design)
                if founded is not None:
                    found.append(pattern)
            return found
        def check_towels(design, patterns):
            size = len(design)
            dp = [False for x in range(size+1)]
            dp[0] = True

            for i in range(1, size + 1):
                for pattern in patterns:
                    if dp[i - len(pattern)] and design[i - len(pattern):i] == pattern:
                        dp[i] = True
                        break
            return dp[size]

        def count_design(design, patterns):
            size = len(design)
            dp = [0 for x in range(size+1)]
            dp[0] = 1

            for i in range(1, size + 1):
                for pattern in patterns:
                    if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                        dp[i] += dp[i - len(pattern)]
            return dp[size]

        def count_combinations():
            ret = 0
            for design in self.designs:
                patterns = get_valid_patterns(design)
                ret += count_design(design, patterns)
            return ret

        def fitting_designs():
            ret = 0
            for design in self.designs:
                patterns = get_valid_patterns(design)
                if check_towels(design, patterns):
                    ret += 1
            return ret

        parse_input()
        print(f"Part 1: {fitting_designs()}")
        print(f"Part 2: {count_combinations()}")

    def day20(self):
        dirs = Directions(self.rows, wall="#")
        self.path_set = set()
        def parse_input():
            self.rows = [ list(row) for row in self.rows ]
        def get_initial_dir(start_x, start_y):
            for d in dirs.directions:
                dx , dy = dirs.coord(d)
                nx, ny = start_x + dx , start_y + dy
                if self.rows[nx][ny] != dirs.wall:
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
                for d in dirs.directions:
                    nx, ny , ndir = dirs.move_from(x, y, d)
                    if 0 <= nx < rows and 0 <= ny < cols \
                        and (nx, ny, ndir) not in visited \
                        and self.rows[nx][ny] != dirs.wall:
                        queue.append((nx, ny, ndir, dist + 1))
                        visited.add((nx, ny, ndir))
                        if (nx, ny, d) not in parent:
                            parent[(nx, ny, ndir)] = (x, y, dir)
            return None , None

        def check_steps(current, new_step):
            c_start = self.steps_count[(current[0], current[1])]
            c_end = self.steps_count[(new_step[0], new_step[1])]
            steps = c_end - c_start
            return steps

        def reachable_nodes(x, y, max_dist, visited):
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

        def cheats_run(path, limit):
            cheats = {}
            visited = set()
            for i , step in enumerate(path):
                x , y , dir = step
                visited.add((x,y))
                nodes = reachable_nodes(x,y,limit,visited)
                for node in nodes:
                    picoseconds = check_steps(step, node) - grid.manhattan_distance((x,y), node)
                    if picoseconds in cheats:
                        a , b = cheats[picoseconds]
                        b.append(node)
                        cheats[picoseconds] = (a+1, b)
                    else:
                        cheats[picoseconds] = (1, [node])
            return cheats

        def picos_below_limit(picos, limit):
            count = 0
            for d in picos:
                if d >= limit:
                    count += picos[d][0]
            return count

        parse_input()
        self.steps_count = defaultdict(int)
        grid = Grid(self.rows)
        self.start = grid.get_elem_pos('S')
        self.end = grid.get_elem_pos('E')
        self.start_dir = get_initial_dir(self.start[0], self.start[1])
        _ , path = shortest_path(self.start[0], self.start[1], self.start_dir)
        picos_part1 = cheats_run(path, 2)
        picos_part2 = cheats_run(path, 20)
        print(f"Part 1: {picos_below_limit(picos_part1, 100)}")
        print(f"Part 2: {picos_below_limit(picos_part2, 100)}")

    def day21(self):
        def parse_input():
            self.codes = self.split_str_by_fun(self.rows, list)

        num_pad = [['7', '8', '9'], ['4', '5','6'],['1', '2', '3'], ['X', '0', 'A']]
        mapping_numpad = {
            '7' : (0,0), '8' : (0,1), '9' : (0,2),
            '4' : (1,0), '5' : (1,1), '6' : (1,2),
            '1' : (2,0), '2' : (2,1), '3' : (2,2),
            'X' : (3,0), '0' : (3,1), 'A' : (3,2)
        }
        num_pad_dirs = Directions(num_pad, wall='X')
        robot_pad = [['X', num_pad_dirs.up, 'A'], [num_pad_dirs.left, num_pad_dirs.down, num_pad_dirs.right]]
        robot_pad_dirs = Directions(robot_pad, wall='X')
        mapping_robotpad = {
            'X' : (0,0), robot_pad_dirs.up : (0,1), 'A' : (0,2),
            robot_pad_dirs.left : (1,0), robot_pad_dirs.down : (1,1), robot_pad_dirs.right : (1,2)
        }

        def shortest_path(key1, key2, pad, gap):
            r1, c1 = pad[key1]
            r2, c2 = pad[key2]
            # Vertical and horizontal movements
            ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
            lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

            # Safe to move vertically first if heading right and corner point isn't the gap
            if c2 > c1 and f"{r2},{c1}" != f"{gap[0]},{gap[1]}":
                return f"{ud}{lr}A"
            # Safe to move horizontally first if corner point isn't the gap
            if f"{r1},{c2}" != f"{gap[0]},{gap[1]}":
                return f"{lr}{ud}A"
            # Must move vertically first because we can't be in the same column as the gap
            return f"{ud}{lr}A"

        def sequences(seq, pad, gap):
            keys = []
            prev_key = "A"
            for key in seq:
                keys.append(shortest_path(prev_key, key, pad, gap))
                prev_key = key
            return keys

        def add_to_freq_table(f_table, sequence):
            f_table[sequence] = f_table.get(sequence, 0) + 1
            return f_table

        def seq_counts(sequence, pad, gap):
            subsequences = sequences(sequence, pad, gap)
            return reduce(add_to_freq_table, subsequences, defaultdict(int))

        def complexity_code(code, num_dir_robots=25):
            f_tables = [ {''.join(sequences(code, mapping_numpad, (3,0))) : 1}]

            for _ in range(num_dir_robots):
                new_f_tables = []
                for f_table in f_tables:
                    new_dic = {}
                    for seq, freq in f_table.items():
                        for sub_seq, sub_freq in seq_counts(seq, mapping_robotpad, (0, 0)).items():
                            new_dic[sub_seq] = new_dic.get(sub_seq, 0) + sub_freq * freq
                    new_f_tables.append(new_dic)
                f_tables = new_f_tables

            def cmplx(freq_table):
                return sum(len(seq) * freq for seq, freq in freq_table.items())

            num = int("".join(code[:-1]))
            return sum(cmplx(f_table) * num for f_table in f_tables)

        def complexities(limit=25):
            ret = 0
            for code in self.codes:
                ret += complexity_code(code, limit)
            return ret

        parse_input()
        start = time.time()
        print(f"Part 1: {complexities(2)}")
        print(f"Part 2: {complexities(25)}")
        end = time.time()
        print(f"Execution time: {end - start} seconds")

    def day22(self):
        self.secrets = {}
        self.prices = {}
        self.max_price = {}
        self.variations = {}
        self.sum_secrets = 0
        self.seqs = {}
        self.max_seq = None
        def parse_input():
            id = 0
            for row in self.rows:
                self.secrets[id] = [int(row)]
                id += 1
        def new_secret(secret):
            step1 = ((secret * 64) ^ secret) % 16777216
            step2 = ((step1 // 32) ^ step1) % 16777216
            step3 = ((step2 * 2048) ^ step2) % 16777216
            return step3
        def get_buyers_secrets(amount):
            last_secret = None
            for i in range(amount):
                print(f"run {i}")
                for id , secrets in self.secrets.items():
                    last_secret = new_secret(secrets[-1])
                    price = last_secret % 10
                    if i == 0:
                        self.secrets[id] = [last_secret]
                        self.prices[id] = [price]
                        self.max_price[id] = price
                    else:
                        self.secrets[id].append(last_secret)
                        self.prices[id].append(price)
                        self.max_price[id] = price if self.max_price[id] < price else self.max_price[id]
                    if i == amount -1:
                        vars_and_max(self.prices[id], id)
                        self.sum_secrets += last_secret
        def vars_and_max(prices, id):
            vars = []
            prev = 0
            visited = set()
            for i , price in enumerate(prices):
                if i == 0:
                    vars.append(0)
                    prev = price
                    continue
                vars.append(price - prev)
                prev = price
                if i >= 4:
                    seq = tuple(vars[i-3:i+1])
                    if seq in visited:
                        continue
                    else:
                        visited.add(seq)
                    if seq in self.seqs:
                        self.seqs[seq]['price'] += price
                        self.seqs[seq]['touches_max'] = self.seqs[seq]['touches_max'] or (price == self.max_price[id])
                    else:
                        self.seqs[seq] = {}
                        self.seqs[seq]['price'] = price
                        self.seqs[seq]['touches_max'] = price == self.max_price[id]
                    new_price = self.seqs[seq]['price']
                    is_max = self.seqs[seq]['touches_max']
                    if self.max_seq is None and is_max:
                        self.max_seq = seq , price
                    elif self.max_seq is None:
                        continue
                    else:
                        _ , maxp_m = self.max_seq
                        if maxp_m < new_price and is_max:
                            self.max_seq = seq , new_price
            return vars
        def check_seq_bananas(seq):
            price = 0
            for id , variation in self.variations.items():
                vars = variation['vars']
                ix = find_sublist_indices(vars, seq)
                if ix is None:
                    continue
                else:
                    price += self.prices[id][ix+3]
            return price
        def find_sublist_indices(main_list, sub_list):
            for i in range(len(main_list) - 3):
                xs = main_list[i:i + 4]
                if xs == sub_list:
                    return i
            return None

        parse_input()
        get_buyers_secrets(2000)
        print(f"Part 1: {self.sum_secrets}")
        print(f"Part 2: {self.max_seq[1]}")

    def day23(self):
        self.graph = defaultdict(set)
        def parse_input():
            for row in self.rows:
                c1 , c2 = re.split("-", row)
                self.graph[c1].add(c2)
                self.graph[c2].add(c1)
        def find_computer_sets_of_3():
            networks = set()
            for pc in self.graph:
                for neighbor in self.graph[pc]:
                    common_neighbors = self.graph[pc] & self.graph[neighbor]
                    for common in common_neighbors:
                        if pc.startswith('t') or neighbor.startswith('t') or common.startswith('t'):
                            triangle = tuple(sorted([pc, neighbor, common]))
                            networks.add(triangle)
            return networks

        def bron_kerbosch(R, P, X, graph, cliques):
            if not P and not X:
                cliques.append(R)
                return
            for node in list(P):
                bron_kerbosch(R | {node}, P & graph[node], X & graph[node], graph, cliques)
                P.remove(node)
                X.add(node)

        # Find all maximal cliques
        def find_maximal_cliques(graph):
            cliques = []
            nodes = set(graph.keys())
            bron_kerbosch(set(), nodes, set(), graph, cliques)
            return cliques

        parse_input()
        sets = find_computer_sets_of_3()
        print(f"Part 1: {len(sets)}")
        cliques = find_maximal_cliques(self.graph)
        max_size = max(len(clique) for clique in cliques)
        largest_cliques = sorted([clique for clique in cliques if len(clique) == max_size][0])
        print(largest_cliques)

    def day24(self):
        def parse_input():
            for row in self.rows:
                id , val = re.split(":", row)
                val = val.strip()
                self.variables[id] = int(val)
                if id.startswith('x'):
                    self.x[id] = int(val)
                else:
                    self.y[id] = int(val)
            regex = r"(\w+)\s+(AND|XOR|OR)\s+(\w+)\s+(->)\s+(\w+)"
            parsed_gates = []
            for gate in self.gates:
                match = re.match(regex, gate)
                if match:
                    exps = list(match.groups())
                    parsed_gates.append(exps)
            self.gates = parsed_gates
        def eval_op(op, e1, e2):
            match op:
                case 'AND': return e1 and e2
                case 'OR': return e1 or e2
                case 'XOR': return e1 ^ e2
        def eval_gates():
            gates = self.gates
            while gates:
                gate = gates.pop(0)
                e1, op, e2, _, out = gate
                if out in self.context:
                    self.context[out] = self.context[out] | { e1 , e2 }
                else:
                    self.context[out] = set()
                    self.context[out] = self.context[out] | { e1 , e2 }
                if e1 in self.variables and e2 in self.variables:
                    if out.startswith('z'):
                        self.out[out] = eval_op(op, self.variables[e1], self.variables[e2])
                    else:
                        self.variables[out] = eval_op(op, self.variables[e1], self.variables[e2])
                    self.var_vals[out] = eval_op(op, self.variables[e1], self.variables[e2])
                else:
                    gates.append(gate)
        def to_int(num):
            binary = ""
            for value in sorted(num, reverse=True):
                binary += str(num[value])
            return int(binary, 2)
        def part1():
            eval_gates()
        def part2():
            preserve = set()
            swap_candidates = set()
            z = to_int(self.x) + to_int(self.y)
            z_bin = list(str(bin(z)[2:]))[::-1]
            expected_out = {}
            for i in range(len(z_bin)):
                if i <= 9:
                    key = f"z0{i}"
                else:
                    key = f"z{i}"
                expected_out[key] = z_bin[i]
            e_int = to_int(expected_out)
            e_bin = bin(e_int)[2:]
            print("expected")
            print(e_bin)
            binary = bin(to_int(self.out))[2:]
            print("computed")
            print(binary)
            result = int(binary, 2) ^ int(e_bin, 2)
            "check bits in the right places"
            xor_result = list(bin(result)[2:].zfill(len(self.out)))[::-1]
            for i , bit in enumerate(xor_result):
                if i <= 9:
                    key = f"z0{i}"
                else:
                    key = f"z{i}"
                if bit == '0':
                    preserve.add(key)
                    preserve = preserve | self.context[key]
                else:
                    swap_candidates.add(key)
                    for var in self.context[key]:
                        if var not in preserve:
                            swap_candidates.add(var)
            by_hand_check = { 'hhp', 'cnq', 'ptm' , 'gfj', 'jdr' , 'mps' , 'snv' , 'jgq' , 'dsj' , 'y14' , 'x14' , 'trn' , 'kvb'}
            swap_candidates = swap_candidates - by_hand_check
            """
            By using the previous code detect swap candidates and manually check the input for patterns we come to the conclusion that
            the changes needed are cnk <-> qwf, vhm <-> z14 , mps <-> z27, msq <-> z39
            Note that XOR and AND connect Xi and Yi with Zi, and the OR connects the sum with the followimg bits, e.g. z40 in the case below
                y39 XOR x39 -> trn
                x39 AND y39 -> mgb
                gpm XOR trn -> msq
                trn AND gpm -> z39
                mgb OR msq -> cqt
            """
            return e_bin == binary

        self.variables = {}
        self.x = {}
        self.y = {}
        self.out = {}
        self.context = {}
        self.var_vals = {}
        parse_input()
        start = time.time()
        part1()
        print(f"Part 1: {to_int(self.out)}")
        print(part2())
        end = time.time()
        print(f"Execution time: {end - start} seconds")

    def day25(self):
        self.keys = []
        self.locks = []
        def get_pins(is_key, columns):
            if is_key:
                pins = []
                for col in columns:
                    ix = re.search(r'\.', col).start()
                    pins.append(ix-1)
                return pins
            else:
                pins = []
                for col in columns:
                    ix = re.search(r'\.', col[::-1]).start()
                    pins.append(ix-1)
                return pins
        def parse_input():
            for schematic in re.split("\n\n", self.rows):
                scheme = re.split("\n", schematic)
                columns = [''.join(column) for column in zip(*scheme)]
                if scheme[0] == ('#' * len(scheme[0])):
                    pins = get_pins(True, columns)
                    self.keys.append(pins)
                else:
                    pins = get_pins(False, columns)
                    self.locks.append(pins)
        def fitting_pairs():
            pairs = [ (x, y) for x in self.keys for y in self.locks ]
            join_p = [ list(zip(p[0],p[1])) for p in pairs ]
            length = len(self.keys[0])
            count = 0
            for xs in join_p:
                if all(val <= length for val in list(map(lambda p : p[0]+p[1] , xs))):
                    count += 1
            return count

        parse_input()
        start = time.time()
        print(f"Part 1: {fitting_pairs()}")
        end = time.time()
        print(f"Execution time: {end - start} seconds")

    def main(self):
        #day = Day()
        #self.rows = day.input.process_data_as_rows(0)
        #self.rows = self.process_data_as_string(file_paths[0], "\n")
        #self.rows = [ list(row) for row in self.rows ]
        #self.columns = self.process_data_as_columns(file_paths[0])
        #day01.day1_part1(self.columns)
        #self.day21()
        day = Day14()
        day.run()

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()