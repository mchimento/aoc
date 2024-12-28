from day import Day
from sympy.ntheory.modular import solve_congruence

class Day14(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)
        self.robots = {}
        for idx, line in enumerate(self.rows, start=1):
            parts = line.split()
            p = tuple(map(int, parts[0].split('=')[1].split(',')))
            p = p[1] , p[0]
            v = tuple(map(int, parts[1].split('=')[1].split(',')))
            v = v[1] , v[0]
            self.robots[idx] = {'p': p, 'v': v}

    def part1(self):
        def step_robot(id, height, width):
            x , y = self.robots[id]['p']
            vx , vy = self.robots[id]['v']
            dx , dy = (x + vx) % height , (y + vy) % width
            self.robots[id]['p'] = dx , dy
        def move_all_robots(time, height, width):
            for id in self.robots:
                for _ in range(time):
                    step_robot(id, height, width)
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
        move_all_robots(100, 103, 101)
        return safety_factor(103, 101)

    def part2(self):
        def check_christmas_tree(height, width):
            """
            by experimenting with draw you can see that:
              - in iteration 6, 107, most robots align in the middle of the grid vertically
              - in iteration 52, 155 most robots align in the middle of the grid horizontally
              in other words:
              - every 103 steps most robots tend to coverge in the y-axis
              - every 101 steps most robots tend to converge in the x-axis
            With this info we can use chinese remainder theorem to in infer at which moment both
            will happen at the same time. At this moment we will have the tree
            time = 5
            while time < 7:
                self.robots = copy.deepcopy(initial_robot)
                self.print_to_file(f"iter {time}", "output.txt")
                time += 1
                move_all_robots(time, height, width)
                draw(height, width)
            """
            remainders = [52, 6]
            moduli = [103, 101]
            result, _ = solve_congruence(*zip(remainders, moduli))
            return result + 1

        return check_christmas_tree(103, 101)