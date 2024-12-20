import argparse
import re
from itertools import groupby
from collections import deque
import heapq
from directions import Directions

class AdventOfCode:

    def process_data_as_columns(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read lines from the file
                data = file.read().strip()
            # Split lines into a list of rows
            rows = data.splitlines()
            # Transpose the rows to columns and join each column into a single string
            columns = [''.join(column) for column in zip(*rows)]
            return columns
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None

    def process_data_as_rows(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read lines from the file
                data = file.read().strip()
            return data.splitlines()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None

    def process_data_as_string(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read lines from the file
                data = file.read().strip().replace("\n","")
            return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None

    def get_initial_pos(self, elem):
        for x in range(0, len(self.rows)):
            for y in range(0, len(self.rows[0])):
                if self.rows[x][y] == elem:
                    return (x, y)
        return None

    def int_list(self, list_string):
        return [int(x) for x in list_string]

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

    def day1_part1(self):
        col0 = sorted(self.columns[0])
        col1 = sorted(self.columns[1])
        res = sum([abs(y-x) for x, y in zip(col0, col1)])
        print(res)

    def day1_part2(self):
        col0 = self.columns[0]
        col1 = self.columns[1]
        res = 0
        for x in col0:
            hit = 0
            for y in col1:
                if x == y:
                    hit += 1
            res += x * hit
        print(res)

    def day2_part1(self):
       def is_sorted_ascending(xs):
           return all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1))
       def is_sorted_descending(xs):
           return all(xs[i] >= xs[i + 1] for i in range(len(xs) - 1))
       def is_safe(xs):
           return all(1 <= abs(xs[i] - xs[i + 1]) <= 3 for i in range(len(xs) - 1))
       def is_sorted(xs):
           return is_sorted_ascending(xs) or is_sorted_descending(xs)
       res = 0
       for row in self.rows:
           if is_safe(row) and is_sorted(row):
               res += 1
       print(res)

    def day2_part2(self):
       def is_sorted_ascending(xs):
           return all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1))
       def is_sorted_descending(xs):
           return all(xs[i] >= xs[i + 1] for i in range(len(xs) - 1))
       def is_safe(xs):
           return all(1 <= abs(xs[i] - xs[i + 1]) <= 3 for i in range(len(xs) - 1))
       def is_sorted(xs):
           return is_sorted_ascending(xs) or is_sorted_descending(xs)
       def dampener(n, xs):
            damped = xs[:n] + xs[n+1:]
            if n + 1 == len(xs):
               return is_safe(damped) and is_sorted(damped)
            else:
               rec = dampener(n + 1, xs)
               return is_safe(damped) and is_sorted(damped) or rec
       res = 0
       for row in self.rows:
            if is_safe(row) and is_sorted(row):
               res += 1
            else:
                if dampener(0, row):
                   res += 1
       print(res)

    def day3_part1(self):
        pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
        matches = re.findall(pattern, self.data)
        results = sum([int(num1) * int(num2) for num1, num2 in matches])
        print(results)

    def day3_part2(self):
        do_p = r'do\(\)'
        dont_p = r'don\'t\(\)'
        pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
        matches = re.findall(pattern, self.data)

        def eval(xs, is_valid):
            if not xs:
                return []
            else:
                hd = xs.pop(0)
                if re.match(do_p, hd):
                    return eval(xs, True)
                elif re.match(dont_p, hd):
                    return eval(xs, False)
                elif is_valid:
                    return eval(xs, is_valid) + [hd]
                else:
                    return eval(xs, is_valid)
        xs = eval(matches, True)

        def evaluate_multiplications(expr_list):
            results = []
            for expr in expr_list:
                numbers = list(map(int, expr.replace('mul(', '').replace(')', '').split(',')))
                results.append(numbers[0] * numbers[1])

            return results
        print(sum(evaluate_multiplications(xs)))

    def day4_part1(self):
        def horizontal(rows, pattern):
            res = 0
            for row in rows:
                matches = re.findall(pattern, row)
                res += len(matches)
            return res
        def vertical(columns, pattern):
            res = 0
            for col in columns:
                matches = re.findall(pattern, col)
                res += len(matches)
            return res
        def mkDiagonal(rows, x, y, limit):
            if x == len(rows):
                return []
            if y == limit:
                return []
            rec = mkDiagonal(rows, x+1, y+1, limit)
            rec.append(rows[x][y])
            return rec
        def mkDiagRow(rows, x, limit):
            res = []
            for y in range(0, limit-1):
                res.append(''.join(mkDiagonal(rows, x, y, limit)[::-1]))
            return res
        def diagonal(rows, limit, pattern):
            res = []
            for x in range(0, len(rows)-1):
                res += mkDiagRow(rows, x, limit)
            ret = 0
            for xs in res:
                ret += len(re.findall(pattern, xs[:4]))
            return ret
        rows = [xs[::-1] for xs in self.rows]

        res = horizontal(self.rows, r'XMAS') \
              + vertical(self.columns, r'XMAS') \
              + diagonal(self.rows, len(self.columns), r'XMAS') \
              + diagonal(rows, len(self.columns), r'XMAS') \
              + horizontal(self.rows, r'SAMX') \
              + vertical(self.columns, r'SAMX') \
              + diagonal(self.rows, len(self.columns), r'SAMX') \
              + diagonal(rows, len(self.columns), r'SAMX')

        print(res)

    def day4_part2(self):
        def mkSquares(rows):
            row0 = rows[0]
            row1 = rows[1]
            row2 = rows[2]
            limit = len(row0)
            squares = []
            for i in range(0, limit-2):
                square = list(row0[:3] + row1[:3] + row2[:3])
                row0 = row0[1:]
                row1 = row1[1:]
                row2 = row2[1:]
                squares.append(square)
            return squares
        def check_square(xs):
            diag1 = xs[0] + xs[4] + xs[8]
            diag2 = xs[2] + xs[4] + xs[6]
            diag1_mas = re.match(diag1, r'MAS') \
                        and re.match(diag2, r'SAM')
            diag2_mas = re.match(diag1, r'SAM') \
                        and re.match(diag2, r'MAS')
            diag3_mas = re.match(diag1, r'MAS') \
                        and re.match(diag2, r'MAS')
            diag4_mas = re.match(diag1, r'SAM') \
                        and re.match(diag2, r'SAM')
            res = diag1_mas or diag2_mas or diag3_mas or diag4_mas
            return res

        squares = []
        limit = len(self.rows)
        res = 0
        for i in range(0, limit-2):
            squares = mkSquares(self.rows[:3])
            for square in squares:
                if check_square(square):
                    res += 1
            self.rows.pop(0)
        print(res)

    def day5_part1(self):
        def val_is_sorted_forward(x, xs, ind):
            for i , val in enumerate(xs):
                if i <= ind:
                    continue
                if val == x:
                    continue
                if not x in self.check_rules:
                    return True
                ordering = self.check_rules[x]
                if val in ordering:
                    continue
                else:
                    return False
            return True
        def val_is_sorted_backwards(x, xs, ind):
            aux = [ val for val in xs[:ind] if x in self.check_rules and val in self.check_rules[x]]
            return not aux

        def val_is_sorted(x, xs, i):
            return val_is_sorted_forward(x, xs, i) and val_is_sorted_backwards(x, xs, i)

        def update_is_sorted(xs):
            res = True
            for i , x in enumerate(xs):
                res = res and val_is_sorted(x, xs, i)
            return res

        def get_middle_value(xs):
            if not xs:
                return None
            if len(xs) % 2 == 1:
                return xs[len(xs) // 2]
            else:
                return xs[len(xs) // 2 - 1: len(xs) // 2 + 1]

        res = []
        for update in self.updates:
            if update_is_sorted(update):
                res.append(get_middle_value(update))
        res = self.int_list(res)
        print(sum(res))

    def day5_part2(self):
        def val_is_sorted_forward(x, xs, ind):
            for i , val in enumerate(xs):
                if i <= ind:
                    continue
                if val == x:
                    continue
                if not x in self.check_rules:
                    return True
                ordering = self.check_rules[x]
                if val in ordering:
                    continue
                else:
                    return False
            return True
        def val_is_sorted_backwards(x, xs, ind):
            aux = [ val for val in xs[:ind] if x in self.check_rules and val in self.check_rules[x]]
            return not aux

        def val_is_sorted(x, xs, i):
            return val_is_sorted_forward(x, xs, i) and val_is_sorted_backwards(x, xs, i)

        def update_is_sorted(xs):
            res = True
            for i , x in enumerate(xs):
                res = res and val_is_sorted(x, xs, i)
            return res

        def get_middle_value(xs):
            if not xs:
                return None
            if len(xs) % 2 == 1:
                return xs[len(xs) // 2]
            else:
                return xs[len(xs) // 2 - 1: len(xs) // 2 + 1]

        def sort_update(xs):
            res = []
            for _ , x in enumerate(xs):
                hits = [ y for y in xs if x in self.check_rules and y in self.check_rules[x] ]
                res.append((x, len(hits)))
            res = sorted(res, key=lambda x: x[1], reverse=True)
            return [x[0] for x in res]

        res = []
        for update in self.updates:
            if not update_is_sorted(update):
                res.append(get_middle_value(sort_update(update)))
        res = self.int_list(res)
        print(sum(res))

    def day6(self):
        def parse_input():
            self.rows = [ list(row) for row in self.rows ]
        dirs = Directions(self.rows, '#')

        def is_inbounds(x, y):
            return 0 <= x < len(self.rows) and 0 <= y < len(self.rows[0])

        def find_path(start, dir, obs=None):
            x, y = start
            visited = set()
            pos_vectors = set()
            pos_vectors.add((x, y, dir))

            while is_inbounds(x, y):
                visited.add((x, y))
                dx, dy = dirs.coord(dir)
                nx, ny = x + dx, y + dy
                with open("output.txt", "a") as file:
                    print(nx, ny, dir, file=file)
                    print(dirs.move_from(x, y, dir), file=file)

                if is_inbounds(nx, ny) and (self.rows[nx][ny] == dirs.wall or (obs and (nx, ny) == obs)):
                    dir = dirs.rotate90_clockwise(dir)
                else:
                    x, y = nx, ny

                pos_vector = (x, y, dir)
                if pos_vector in pos_vectors:
                    return True, visited
                pos_vectors.add(pos_vector)

            return False, visited

        parse_input()
        start = self.get_initial_pos(dirs.up)

        _, visited = find_path(start, dirs.up)
        print(f"Part 1: {len(visited)}")

        result = 0
        obstacles = visited - {start}
        for obs in obstacles:
            if find_path(start, dirs.up, obs)[0]:
                result += 1
        print(f"Part 2: {result}")

    def day7(self):
        def parse_input():
            rows = []
            for row in self.rows:
                parts = row.split(':')
                test = int(parts[0].strip())
                values = [int(num) for num in parts[1].strip().split()]
                result = (test, values)
                rows.append(result)
            self.rows = rows
            self.print_rows(self.rows)
        def add(x, y):
            return x+y
        def mult(x, y):
            return x*y
        def app(x, y):
            return int(str(x)+str(y))
        operations = [add, mult, app]
        def eval_all_exps(values):
            if len(values) == 1:
                return values
            val = values.pop()
            rec = eval_all_exps(values)
            exps = []
            for op in operations:
                for exp in rec:
                    exps.append(op(exp, val))
            return exps

        parse_input()
        res = 0
        for row in self.rows:
            if row[0] in eval_all_exps(row[1]):
                res += row[0]
        print(res)

    def day8(self):
        map = {}
        self.highest_id = 0
        def parse_input():
            self.rows = [int(val) for val in self.rows[0]]
        def is_even(n):
            return n % 2 == 0
        def block_map():
            res = []
            id = 0
            for i , file in enumerate(self.rows):
                if is_even(i):
                    map[id] = file
                    for _ in range(file):
                        res.append(id)
                    id += 1
                else:
                    for _ in range(file):
                        res.append(".")
            self.highest_id = id-1
            self.rows = res
        def check_sum():
            res = 0
            back = len(self.rows) - 1
            for i , val in enumerate(self.rows):
                if i > back:
                    break
                if val != '.':
                    res += i * val
                else:
                    c = '.'
                    while c == '.':
                        c = self.rows[back]
                        if c == '.':
                            back -=1
                        else:
                            res += i * c
                            back -=1
            return res
        def get_id_index(id):
            for x in range(len(self.rows)):
                if self.rows[x] == id:
                    return x
            else:
                return None
        def check_sum_whole_file():
            res = 0
            for id in range(self.highest_id, 0, -1):
                for i , val in enumerate(self.rows):
                    if val == id:
                        break
                    if val != '.':
                        continue
                    space = 1
                    c = '.'
                    ix = i+1
                    while c == '.':
                        if ix >= len(self.rows):
                            break
                        c = self.rows[ix]
                        if c == '.':
                            space += 1
                            ix += 1
                    size = map[id]
                    if size <= space:
                        back = get_id_index(id)
                        for y in range(size):
                            self.rows[i+y] = id
                            self.rows[back+y] = '.'
                        break
            return res

        parse_input()
        block_map()
        print(f"part 1: {check_sum()}")
        check_sum_whole_file()
        res = 0
        for i , val in enumerate(self.rows):
            if  val == '.':
                continue
            res += i * val
        print(f"part 2: {res}")

    def day10(self):
        def parse_input():
            for x in range(0, len(self.rows)):
                for y in range(0, len(self.rows[0])):
                    self.rows[x][y] = int(self.rows[x][y])
        def get_trailheads():
            res = []
            for x in range(0, len(self.rows)):
                for y in range(0, len(self.rows[0])):
                    if self.rows[x][y] == 0:
                        res.append((x, y))
            return res
        def reachable_coords(x, y, val):
            reachables = []
            if 0 <= x - 1  < len(self.rows):
                if self.rows[x-1][y] == val:
                    reachables.append((x-1, y))
            if 0 <= x + 1  < len(self.rows):
                if self.rows[x+1][y] == val:
                    reachables.append((x+1, y))
            if 0 <= y - 1  < len(self.rows[0]):
                if self.rows[x][y-1] == val:
                    reachables.append((x, y-1))
            if 0 <= y + 1  < len(self.rows[0]):
                if self.rows[x][y+1] == val:
                    reachables.append((x, y+1))
            return reachables
        def check_trailhead(trailhead):
            paths = [[(trailhead[0], trailhead[1])]]
            for val in range(1, 10):
                new_paths = []
                for path in paths:
                    x , y = path[len(path)-1]
                    next_positions = reachable_coords(x, y, val)
                    if not next_positions:
                        continue
                    for pos in next_positions:
                        new_path = path.copy()
                        new_path.append(pos)
                        new_paths.append(new_path)
                paths = new_paths
            return paths
        def trials_score(trials):
            reached = set()
            for trial in trials:
                reached.add(trial[len(trial)-1])
            return len(reached)

        parse_input()
        trailheads = get_trailheads()
        res = 0
        for trailhead in trailheads:
            res += trials_score(check_trailhead(trailhead))
        print(f"Part 1: {res}")
        res = 0
        for trailhead in trailheads:
            res += len(check_trailhead(trailhead))
        print(f"Part 2: {res}")

    def day12(self):
        def check_plot_after(x, y, plant):
            if y + 1 < len(self.columns):
                return plant == self.rows[x][y+1]
            else:
                return False
        def check_plot_before(x, y, plant):
            if y - 1 >= 0:
                return plant == self.rows[x][y-1]
            else:
                return False
        def check_plot_below(x, y, plant):
            if x + 1 < len(self.rows):
                return plant == self.rows[x+1][y]
            else:
                return False
        def check_plot_above(x, y, plant):
            if x - 1 >= 0:
                return plant == self.rows[x-1][y]
            else:
                return False
        def check_area(x, y, plant):
            self.rows[x][y] = None
            analyse = [(x,y)]
            region = [(x,y)]
            while(analyse != []):
                x , y = analyse.pop(0)
                if check_plot_after(x, y, plant):
                    region.append((x,y+1))
                    analyse.append((x,y+1))
                    self.rows[x][y+1] = None
                if check_plot_before(x, y, plant):
                    region.append((x,y-1))
                    analyse.append((x,y-1))
                    self.rows[x][y-1] = None
                if check_plot_below(x, y, plant):
                    region.append((x+1,y))
                    analyse.append((x+1,y))
                    self.rows[x+1][y] = None
                if check_plot_above(x, y, plant):
                    region.append((x-1,y))
                    analyse.append((x-1,y))
                    self.rows[x-1][y] = None
            return region

        def getRegions():
            regions = []
            plant = None
            for x in range(0, len(self.rows)):
                for y in range(0, len(self.columns)):
                    if self.rows[x][y] is None:
                        continue
                    plant = self.rows[x][y]
                    area = check_area(x, y, plant)
                    regions.append((area, plant))
            return regions

        def area(region):
            return len(region)
        def perimeter(region):
            total = 4 * len(region)
            for (x , y) in region:
                if (x, y+1) in region:
                    total -= 1
                if (x+1, y) in region:
                    total -= 1
                if (x, y-1) in region:
                    total -= 1
                if (x-1, y) in region:
                    total -= 1
            return total
        def sides(region):
            print(region)
            print(f"perimeter: {perimeter(region[0])}")
            return 1

        regions = getRegions()
        part1 = 0
        part2 = 0
        for region in regions:
            part1 += area(region[0]) * perimeter(region[0])
            part2 += area(region[0]) * sides(region)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")

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
                    while current is not None:
                        path.append(current)
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

        def cheat_to_path(x, y, dir, path, visited):
            dc = dirs.rotate90_clockwise(dir)
            dac = dirs.rotate90_anticlockwise(dir)
            dinv = dirs.turn_around(dir)
            with open("output.txt", "a") as file:
                print(f"Candidaties position to jump {(x, y, dc)} and {(x, y, dac)} and {(x, y, dinv)}", file=file)
            if (x, y, dc) in path and not (x, y, dc) in visited:
                return (x, y, dc)
            elif (x, y, dac) in path and not (x, y, dac) in visited:
                return (x, y, dac)
            elif (x, y, dinv) in path and not (x, y, dinv) in visited:
                return (x, y, dinv)
            else:
                return None

        def apply_cheat(x, y, dir, path, visited):
            rows = len(self.rows) - 1
            cols = len(self.rows[0]) - 1
            with open("output.txt", "a") as file:
                print(f"Apply from node {(x,y)}", file=file)
            # one step
            dx , dy = dirs.coord(dir)
            nx, ny = x + dx , y + dy
            if 0 <= nx < rows and 0 <= ny < cols and self.rows[nx][ny] == dirs.wall:
                #step two
                nx, ny = nx + dx , ny + dy
                if 0 <= nx < rows and 0 <= ny < cols and self.rows[nx][ny] == dirs.wall:
                    #step three
                    nx, ny = nx + dx , ny + dy
                    if 0 <= nx < rows and 0 <= ny < cols and self.rows[nx][ny] == dirs.wall:
                        return None , None
                    elif 0 <= nx < rows and 0 <= ny < cols:
                        with open("output.txt", "a") as file:
                            print(f"Check cheat at {nx, ny, dir}", file=file)
                        return cheat_to_path(nx, ny, dir, path, visited) , 3
                    else:
                        return None , None
                elif 0 <= nx < rows and 0 <= ny < cols:
                    with open("output.txt", "a") as file:
                            print(f"Check cheat at {nx, ny, dir}", file=file)
                    return cheat_to_path(nx, ny, dir, path, visited) , 2
                else:
                    return None , None
            return None , None

        def check_step_saved(path, ix, cell, steps_taken):
            cell_ind = -1
            unvisited = path[ix+1:]
            for i , step in enumerate(unvisited):
                if step != cell:
                    continue
                cell_ind = i
            unvisited = unvisited[:cell_ind]
            with open("output.txt", "a") as file:
                print(f"Before steps {cell_ind}", file=file)
                print(f"Now steps {steps_taken}", file=file)
            return cell_ind - steps_taken + 1

        def cheats_run(path):
            cheats = {}
            for i , step in enumerate(path):
                x , y , dir = step
                with open("output.txt", "a") as file:
                    print(f"\ncheck step {x , y , dir}, iter {i}", file=file)
                for d in dirs.directions:
                    if dirs.turn_around(dir) == d:
                        continue
                    dx , dy = dirs.coord(d)
                    nx, ny = x + dx , y + dy
                    if  0 <= nx < len(self.rows) - 1 and 0 <= ny < len(self.rows[0]) - 1 \
                        and self.rows[nx][ny] == dirs.wall:
                        with open("output.txt", "a") as file:
                            print(f"Candidate direction for cheat {d}, from Node {(x,y)}", file=file)
                        visited = path[:i+1]
                        new_step , steps_taken = apply_cheat(x, y, d, path, visited)
                        if new_step is not None:
                            picoseconds = check_step_saved(path, i, new_step, steps_taken)
                            with open("output.txt", "a") as file:
                                print(f"Jump to step {new_step}, reached in {steps_taken} steps.", file=file)
                                print(f"Savings: {picoseconds} steps.", file=file)
                            if picoseconds in cheats:
                                xs = cheats[picoseconds]
                                xs.append(new_step)
                                cheats[picoseconds] = xs
                            else:
                                cheats[picoseconds] = [new_step]
                        with open("output.txt", "a") as file:
                            print(f"No cheats applicable for candidate", file=file)
            return cheats

        def picos_below_limit(picos, limit):
            count = 0
            for d in picos:
                if d >= limit:
                    count += len(picos[d])
            return count

        parse_input()
        start_x , start_y = self.get_initial_pos('S')
        print(start_x , start_y)
        dir = get_initial_dir(start_x, start_y)
        cost , path = shortest_path(start_x, start_y, dir)
        print(path)
        saved_picos = cheats_run(path)
        #for x , y, dir in path:
        #    self.rows[x][y] = 'O'
        #self.rows[start_x][start_y] = 'S'
        #with open("output.txt", "a") as file:
        #    for row in self.rows:
        #        print(f"{"".join(row)}", file=file)
        #print(saved_picos)
        sorted_dict = {k: saved_picos[k] for k in sorted(saved_picos)}
        print(f"Part 1: {picos_below_limit(saved_picos, 100)}")

    def alt(self):
        def parse_input():
            self.rows = [ list(row) for row in self.rows ]
        ds = ((1,0),(-1,0),(0,1),(0,-1))
        def bfs(p):
            distMap = {p:0}
            queue = [p]
            for r,c in queue:
                d = distMap[(r,c)]
                for dr,dc in ds:
                    nr,nc = r+dr,c+dc
                    if (nr,nc) not in distMap and self.rows[nr][nc] != '#':
                        queue.append((nr,nc))
                        distMap[(nr,nc)] = d+1
            return distMap

        parse_input()
        start = self.get_initial_pos('S')
        startMap = bfs(start)

        def Cheats():
            cheats = {}
            for r,c in startMap:
                for dr,dc in ds:
                    nr,nc = r+2*dr,c+2*dc
                    if (nr,nc) in startMap:
                        if startMap[(r,c)] > startMap[(nr,nc)]:
                            nn =  startMap[(r,c)] - startMap[(nr,nc)] -2
                            if nn > 0:
                                cheats[((nr,nc),(r,c))] = nn
            return cheats

        cheats = Cheats()
        p1 = 0
        sorted_dict = {k: v for k, v in sorted(cheats.items(), key=lambda item: item[1])}
        with open("output.txt", "a") as file:
            for d in sorted_dict:
                print(f"{sorted_dict[d]}:{d}", file=file)
        print(sorted_dict)
        for i in cheats:
            n = cheats[i]
            if n >= 100:p1 += 1
        print(p1)

    def main(self):
        """
        Main function to process command-line arguments and handle the file input.
        """
        parser = argparse.ArgumentParser(description="Process a file.")
        parser.add_argument("file_paths", nargs="+", type=str, help="Path to the input file")

        args = parser.parse_args()
        file_paths = args.file_paths

        # Process the file and get columns
        self.rows = self.process_data_as_rows(file_paths[0])
        #self.rows = [ list(row) for row in self.rows ]
        #self.columns = self.process_data_as_columns(file_paths[0])

        self.day20()

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()