import argparse
import re
from itertools import groupby
from collections import deque
import heapq
from directions import Directions
from grid import Coordinate, Grid
import time
from collections import Counter
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
from sympy import solve, Symbol

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

    def process_data_as_string(self, file_path, eof_by=""):
        try:
            with open(file_path, 'r') as file:
                # Read lines from the file
                data = file.read().strip().replace("\n",eof_by)
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

    def print_to_file(self, s, file_path, type='a'):
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
        return

    def day9(self):
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

    def day11(self):
        def parse_input():
            self.rows = self.rows[0].split(" ")
        def count_stones(blinks):
            stones = self.int_list(self.rows)
            stone_counts = Counter(stones)
            for _ in range(blinks):
                new_counts = Counter()
                for stone, count in stone_counts.items():
                    if stone == 0:
                        new_counts[1] += count
                    elif len(str(stone)) % 2 == 0:
                        half_len = len(str(stone)) // 2
                        left = int(str(stone)[:half_len])
                        right = int(str(stone)[half_len:])
                        new_counts[left] += count
                        new_counts[right] += count
                    else:
                        new_counts[stone * 2024] += count
                stone_counts = new_counts

            return sum(stone_counts.values())

        parse_input()
        start = time.time()
        amount = count_stones(75)
        print(f"Part 1: {amount}")
        end = time.time()
        print(f"Execution time: {end - start} seconds")

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

    def day13(self):
        def parse_input():
            pattern = re.compile(r'(Button [A-B]: )?(X[+-]?\d+),\s*(Y[+-]?\d+)|Prize: (X=\d+),\s*(Y=\d+)')
            matches = pattern.findall(self.rows)
            parsed_elements = []

            for match in matches:
                # If it's a Button match (Button A or Button B)
                if match[0]:
                    button, x_value, y_value, _, _ = match
                    button_label = button.split()[1]
                    x_var, x_num = x_value.split('+') if '+' in x_value else x_value.split('-')
                    y_var, y_num = y_value.split('+') if '+' in y_value else y_value.split('-')

                    x_num = int(x_num) if x_num != '' else 0
                    y_num = int(y_num) if y_num != '' else 0

                    parsed_elements.append([button_label, x_var, x_num, y_var, y_num])
                elif match[3]:
                    # If it's a Prize match
                    x_value, y_value = match[3], match[4]
                    x_var, x_num = x_value.split('=')
                    y_var, y_num = y_value.split('=')

                    parsed_elements.append([x_var, int(x_num), y_var, int(y_num)])

            problems = []
            for i in range(0, len(parsed_elements), 3):
                problem = [parsed_elements[i], parsed_elements[i+1], parsed_elements[i+2]]
                problems.append(problem)

            return problems

        def solve_lp_int(x1, y1, x2, y2, x, y):
            problem = LpProblem("Maximize_X2_Y2", LpMaximize)

            # Define integer variables
            X1 = LpVariable("X1", lowBound=0, upBound=100, cat="Integer")
            X2 = LpVariable("X2", lowBound=0, upBound=100, cat="Integer")
            Y1 = LpVariable("Y1", lowBound=0, upBound=100, cat="Integer")
            Y2 = LpVariable("Y2", lowBound=0, upBound=100, cat="Integer")

            problem += X2 + Y2, "Objective"
            problem += x1 * X1 + x2 * X2 == x, "Constraint_X"
            problem += y1 * Y1 + y2 * Y2 == y, "Constraint_Y"
            problem += X1 == Y1, "Constraint_X1_equals_Y1"
            problem += X2 == Y2, "Constraint_X2_equals_Y2"

            solver = PULP_CBC_CMD(msg=False)
            status = problem.solve(solver)

            if status == 1:
                print("Optimized Solution:")
                print(f"  X1 = {X1.varValue}")
                print(f"  X2 = {X2.varValue}")
                print(f"  Y1 = {Y1.varValue}")
                print(f"  Y2 = {Y2.varValue}")
                return X1.varValue , X2.varValue
            else:
                print("Optimization failed.")
                return None , None

        def solve_lp_int_numpy(x1, y1, x2, y2, x, y):
            a = Symbol("a", integer=True)
            b = Symbol("b", integer=True)
            # Remove for part 1
            x += 10000000000000
            y += 10000000000000
            roots = solve(
                [a * x1 + b * x2 - x, a * y1 + b * y2 - y],
                [a, b],
            )
            return roots[a] * 3 + roots[b] if roots else 0

        def find_tokens(nlp):
            final = 0
            for problem in nlp:
                A = problem[0]
                B = problem[1]
                X = problem[2]
                a_push , b_push = solve_lp_int(A[2], A[4], B[2], B[4], X[1], X[3])
                if a_push is not None:
                    final +=  a_push * 3 + b_push
            return final

        def find_tokens_unbound(nlp):
            final = 0
            for problem in nlp:
                A = problem[0]
                B = problem[1]
                X = problem[2]
                final += solve_lp_int_numpy(A[2], A[4], B[2], B[4], X[1], X[3])
            return final

        nlp = parse_input()
        print(f"Part 1: {find_tokens(nlp)}")
        print(f"Part 2: {find_tokens_unbound(nlp)}")

    def day14(self):
        self.robots = {}
        self.robots_len = 0
        def parse_input():
            lines = self.rows.strip().split("\n")
            for idx, line in enumerate(lines, start=1):
                parts = line.split()
                p = tuple(map(int, parts[0].split('=')[1].split(',')))
                p = p[1] , p[0]
                v = tuple(map(int, parts[1].split('=')[1].split(',')))
                v = v[1] , v[0]
                self.robots[idx] = {'p': p, 'v': v}
                self.robots_len += 1

        def step_robot(id, height, width):
            x , y = self.robots[id]['p']
            vx , vy = self.robots[id]['v']
            dx , dy = (x + vx) % height , (y + vy) % width
            self.robots[id]['p'] = dx , dy
        def move_robot(id, time, height, width):
            for _ in range(time):
                step_robot(id, height, width)
        def move_all_robots(time, height, width):
            for id in self.robots:
                move_robot(id, time, height, width)
        def safety_factor(height, width):
            mid_h = (height - 1) // 2
            mid_v = (width - 1) // 2
            q1 , q2 ,q3 , q4 = 0 , 0 , 0 , 0
            for id in self.robots:
                x , y = self.robots[id]['p']
                if x < mid_h and y < mid_v: q1 += 1
                elif x < mid_h and y > mid_v: q2 += 1
                elif x > mid_h and y < mid_v: q3 += 1
                elif x > mid_h and y > mid_v: q4 += 1
                else: continue
            return q1 * q2 * q3 * q4

        def chek_christmas_tree(height, width):
            def all_pos_unique(positions_count):
                return all(count == 1 for count in positions_count.values())
            time = 1647
            self.robots = initial_robot.copy()
            while time < 3:
                time += 1
                positions_count = Counter()
                print(f"check time {time}")
                move_all_robots(time, height, width)
                for _, data in self.robots.items():
                    positions_count[data['p']] += 1
                print(self.robots)
                print(positions_count)
                if all_pos_unique(positions_count):
                    return time
            return -1

        parse_input()
        self.print_to_file(str(self.robots), "output.txt")
        initial_robot = self.robots.copy()
        start = time.time()
        move_all_robots(100, 103, 101)
        sf = safety_factor(103, 101)
        #print(f"Part 1: {sf}")
        ch_time = chek_christmas_tree(103, 101)
        print(f"Part 2: {ch_time}")
        end = time.time()
        print(f"Execution time: {end - start} seconds")

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
            #with open("output.txt", "a") as file:
            #    print(f"Candidaties position to jump {(x, y, dc)} and {(x, y, dac)} and {(x, y, dinv)}", file=file)
            if (x, y, dc) in path and not (x, y, dc) in visited:
                return (x, y, dc)
            elif (x, y, dac) in path and not (x, y, dac) in visited:
                return (x, y, dac)
            elif (x, y, dinv) in path and not (x, y, dinv) in visited:
                return (x, y, dinv)
            else:
                return None

        def cheat_step(x, y, dir, path, visited, limit):
            rows = len(self.rows) - 1
            cols = len(self.rows[0]) - 1
            #with open("output.txt", "a") as file:
            #    print(f"Apply from node {(x,y)}", file=file)
            x_iter , y_iter = x , y
            for i in range(limit+1):
                dx , dy = dirs.coord(dir)
                nx, ny = x_iter + dx , y_iter + dy
                if 0 <= nx < rows and 0 <= ny < cols and self.rows[nx][ny] == dirs.wall:
                    x_iter , y_iter = nx , ny
                    continue
                elif 0 <= nx < rows and 0 <= ny < cols:
                    #with open("output.txt", "a") as file:
                    #    print(f"Check cheat at {nx, ny, dir}", file=file)
                    return cheat_to_path(nx, ny, dir, path, visited) , i+1
                else:
                    break
            return None , None

        def cheat_step_new(candidate, steps, path, visited):
            rows = len(self.rows) - 1
            cols = len(self.rows[0]) - 1
            x , y, dir, _ = candidate
            hitted_wall = set()
            cheats = set()
            with open("output.txt", "a") as file:
                print(f"checking candidate {x , y , dir}", file=file)
            for d in dirs.directions:
                dx , dy = dirs.coord(d)
                nx, ny = x + dx , y + dy
                with open("output.txt", "a") as file:
                    print(f"Check cheat at {nx, ny, d}", file=file)
                if 0 <= nx < rows and 0 <= ny < cols and self.rows[nx][ny] == dirs.wall:
                    with open("output.txt", "a") as file:
                        print(f"Hits wall", file=file)
                    hitted_wall.add((nx, ny, d, steps))
                elif 0 <= nx < rows and 0 <= ny < cols:
                    with open("output.txt", "a") as file:
                        print(f"Getting cheat", file=file)
                    cheat = cheat_to_path(nx, ny, d, path, visited)
                    if cheat is not None:
                        xc , yc, dirc = cheat
                        with open("output.txt", "a") as file:
                            print(f"Cheat at {xc , yc, dirc}", file=file)
                        cheats.add((xc , yc, dirc, steps))
                else:
                    with open("output.txt", "a") as file:
                        print(f"No new candidates", file=file)
                    continue
            return cheats , hitted_wall

        def cheat_path(x , y, dir, limit, path, visited):
            candidates = set()
            candidates = [(x, y, dir, 0)]
            cheats = set()
            for i in range(limit):
                with open("output.txt", "a") as file:
                        print(f"cheat_path iter {i}", file=file)
                if not candidates:
                    break
                new_candidates = set()
                for candidate in candidates:
                    new_steps , hitted_wall = cheat_step_new(candidate, i+1, path, visited)
                    new_candidates = new_candidates | hitted_wall
                    with open("output.txt", "a") as file:
                        print(f"New candidates {hitted_wall}", file=file)
                        print(f"New cheats {new_steps}", file=file)
                    cheats = cheats | new_steps
                candidates = new_candidates
            return cheats

        def check_step_saved(path, ix, cell, steps_taken):
            cell_ind = -1
            unvisited = path[ix+1:]
            for i , step in enumerate(unvisited):
                if step != cell:
                    continue
                cell_ind = i
            #with open("output.txt", "a") as file:
            #    print(f"Before steps {cell_ind}", file=file)
            #    print(f"Now steps {steps_taken}", file=file)
            return cell_ind - steps_taken + 1

        def cheats_run(path, limit):
            cheats = {}
            for i , step in enumerate(path):
                x , y , dir = step
                #with open("output.txt", "a") as file:
                #    print(f"\ncheck step {x , y , dir}, iter {i}", file=file)
                visited = path[:i+1]
                for d in dirs.directions:
                    new_step , steps_taken = cheat_step(x, y, d, path, visited, limit)
                    if new_step is not None:
                        picoseconds = check_step_saved(path, i, new_step, steps_taken)
                        #with open("output.txt", "a") as file:
                        #    print(f"Jump to step {new_step}, reached in {steps_taken} steps.", file=file)
                        #    print(f"Savings: {picoseconds} steps.", file=file)
                        if picoseconds in cheats:
                            a , b = cheats[picoseconds]
                            b.append(new_step)
                            cheats[picoseconds] = (a+1, b)
                        else:
                            cheats[picoseconds] = (1, [new_step])
                    #with open("output.txt", "a") as file:
                    #    print(f"No cheats applicable for candidate", file=file)
            return cheats

        def check_step_saved_new(path, ix, cheats):
            cell_ind = -1
            unvisited = path[ix+1:]
            picos =[]
            for cheat in cheats:
                x , y, dir, n = cheat
                for i , step in enumerate(unvisited):
                    if step != (x, y, dir):
                        continue
                    cell_ind = i
                picos.append((cell_ind - n + 1, (x,y)))
            return picos

        def cheats_run_new(path, limit):
            cheats = {}
            for i , step in enumerate(path):
                x , y , dir = step
                with open("output.txt", "a") as file:
                    print(f"\ncheck step {x , y , dir}, iter {i}", file=file)
                visited = path[:i+1]
                cheats_found = cheat_path(x, y, dir, limit, path, visited)
                picoseconds = check_step_saved_new(path, i, cheats_found)
                with open("output.txt", "a") as file:
                    print(f"Cheats found {cheats_found}", file=file)
                    print(f"Steps calculation: {picoseconds}", file=file)
                for picos , new_step in picoseconds:
                    if picos in cheats:
                        a , b = cheats[picos]
                        b.append(new_step)
                        cheats[picos] = (a+1, b)
                    else:
                        cheats[picos] = (1, [new_step])
            with open("output.txt", "a") as file:
                print(f"No cheats applicable for candidate", file=file)
            return cheats

        def picos_below_limit(picos, limit):
            count = 0
            for d in picos:
                if d >= limit:
                    count += picos[d]
            return count

        parse_input()
        self.start = self.get_initial_pos('S')
        self.start_dir = get_initial_dir(self.start[0], self.start[1])
        _ , path = shortest_path(self.start[0], self.start[1], self.start_dir)
        saved_picos = cheats_run_new(path, 2)
        sorted_dict = {k: saved_picos[k] for k in sorted(saved_picos)}
        print(sorted_dict)
        print(f"Part 1: {picos_below_limit(saved_picos, 100)}")
        print(f"Part 1: {"coming soon"}")

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
        num_pad_grid = Grid(num_pad)
        num_pad_dirs = Directions(num_pad, wall='X')

        robot_pad = [['X', num_pad_dirs.up, 'A'], [num_pad_dirs.left, num_pad_dirs.down, num_pad_dirs.right]]
        robot_pad_grid = Grid(robot_pad)
        robot_pad_dirs = Directions(robot_pad, wall='X')
        mapping_robotpad = {
            'X' : (0,0), robot_pad_dirs.up : (0,1), 'A' : (0,2),
            robot_pad_dirs.left : (1,0), robot_pad_dirs.down : (1,1), robot_pad_dirs.right : (1,2)
        }

        def transform_coord(path, dirs):
            keep = []
            for i in range(len(path)-1):
                if path[i][0] == path[i+1][0] + 1:
                    keep.append(dirs.up)
                elif path[i][0] == path[i+1][0] - 1:
                    keep.append(dirs.down)
                elif path[i][1] == path[i+1][1] - 1:
                    keep.append(dirs.right)
                else:
                    keep.append(dirs.left)
            keep.append('A')
            return keep

        def numpad_shortest_paths(code):
            ret = []
            current = mapping_numpad['A']
            for end in code:
                _ , paths = num_pad_grid.shortest_paths(current, end, num_pad, num_pad_dirs)
                keep = filter_chunks(list(map(lambda xs: transform_coord(xs, num_pad_dirs), paths)))
                if not ret:
                    ret = keep
                else:
                    ret = [xs + ys for xs in ret for ys in keep]
                current = mapping_numpad[end]
            return filter_min(ret)

        def filter_min(paths):
            length = 0
            keep = []
            for path in paths:
                path_len = len(path)
                if length == 0:
                    length = path_len
                    keep.append(path)
                else:
                    if path_len > length:
                        continue
                    else:
                        keep.append(path)
            return keep

        def filter_consecutive_adj(chunks):
            def points(dir):
                match dir:
                    case num_pad_dirs.right: return 4
                    case num_pad_dirs.up: return 3
                    case num_pad_dirs.down: return 2
                    case num_pad_dirs.left: return 1
                    case _: return 5
            def count_adj(xs):
                count = 0
                for i in range(len(xs)-1):
                    if xs[i] == xs[i+1]:
                        count += points(xs[i])
                return count
            keep = []
            max_adj = 0
            for chunk in chunks:
                n = count_adj(chunk)
                if n > 0:
                    if n > max_adj:
                        max_adj = n
                        keep = [chunk]
                    elif n == max_adj:
                        keep.append(chunk)
                    else:
                        continue
            if not keep:
                return chunks
            else:
                return keep

        def filter_on_priority_adj(chunks):
            def is_adj(dir1, dir2):
                x1 , y1 = mapping_robotpad[dir1]
                x2 , y2 = mapping_robotpad[dir2]
                if dir1 == dir2:
                    return True
                else:
                    return x1 == x2 and (y1 + 1 == y2 or y1 == y2 + 1) \
                           or y1 == y2 and (x1 + 1 == x2 or x1 == x2 + 1)
            def adj_amount(chunk):
                ret = 0
                for i in range(len(chunk)-1):
                    if is_adj(chunk[i], chunk[i+1]):
                        ret += 1
                        if chunk[i] == 'A':
                            ret += 1
                return ret
            keep = []
            adj = 0
            for i in range(len(chunks)):
                if not keep:
                    keep = [chunks[i]]
                    adj = adj_amount(chunks[i])
                    #print(f"adj amount intit {adj}")
                    continue
                adj_amount_ch = adj_amount(chunks[i])
                #print(f"adj amount {adj_amount_ch}")
                if adj_amount_ch > adj:
                    adj = adj_amount_ch
                    keep = [chunks[i]]
                elif adj_amount_ch < adj:
                    continue
                else:
                    keep.append(chunks[i])
            #print(keep)
            return keep

        def filter_chunks(chunks):
            keep = []
            "chunks with more adjacents arrows in the same direction are cheaper to analyse"
            keep = filter_consecutive_adj(chunks)
            "prioritize adjcent arrows"
            keep = filter_on_priority_adj(keep)
            return keep

        def robotpad_shortest_paths(numpad_paths):
            ret = []
            current = mapping_robotpad['A']
            min_length = None
            for path in numpad_paths:
                aux = []
                current_len = 0
                for end in path:
                    _ , paths = robot_pad_grid.shortest_paths(current, end, robot_pad, robot_pad_dirs)
                    if paths:
                        keep = filter_chunks(list(map(lambda xs: transform_coord(xs, robot_pad_dirs), paths)))
                        if not aux:
                            aux = keep
                        else:
                            aux = [xs + ys for xs in aux for ys in keep]
                        current_len += len(keep[0])
                    if  min_length is not None and current_len > min_length:
                        break
                    current = mapping_robotpad[end]
                if min_length is None:
                    min_length = len(aux[0])
                    ret += aux
                    continue
                if current_len < min_length:
                    min_length = current_len
                    ret = []
                ret += aux
            return filter_chunks(filter_min(ret))

        def complexities(limit=2):
            ret = 0
            for code in self.codes:
                robot_paths = filter_chunks(numpad_shortest_paths(code))
                print(robot_paths)
                for _ in range(limit):
                    print(f"before {len(robot_paths)}")
                    robot_paths = filter_chunks(robotpad_shortest_paths(robot_paths))
                    #self.print_rows(robot_paths)
                    print(f"after {len(robot_paths)}")
                min_length = len(robot_paths[0])
                code.pop()
                code_int = int("".join(code))
                print(f"complexity is {min_length} * {code_int}")
                ret += min_length * code_int
            return ret

        parse_input()
        start = time.time()
        #print(f"Part 1: {complexities(2)}")
        print(f"Part 2: {complexities(2)}")
        end = time.time()
        print(f"Execution time: {end - start} seconds")

    def main(self):
        """
        Main function to process command-line arguments and handle the file input.
        """
        parser = argparse.ArgumentParser(description="Process a file.")
        parser.add_argument("file_paths", nargs="+", type=str, help="Path to the input file")

        args = parser.parse_args()
        file_paths = args.file_paths

        # Process the file and get columns
        #self.rows = self.process_data_as_rows(file_paths[0])
        self.rows = self.process_data_as_string(file_paths[0], "\n")
        #self.rows = [ list(row) for row in self.rows ]
        #self.columns = self.process_data_as_columns(file_paths[0])

        self.day14()

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()