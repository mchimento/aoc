from day import Day
import numpy as np
from functools import reduce

class Day06(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_rows(0)
        self.time = self.input.int_list([ xs.strip() for xs in input[0].split(":")[1].strip().split("  ") if xs != ""])
        self.dist = self.input.int_list([ xs.strip() for xs in input[1].split(":")[1].strip().split("  ")])
        self.input = list(zip(self.time, self.dist))

    def part1(self):
        def find_interval(time, distance):
            # Calculate the roots of the quadratic equation
            # (time - x)*x >= distance and 0 <= x <= time
            # note that argument distance has to be the input distance + 1 as we have to go farther than it
            a = 1
            b = -time
            c = distance
            discriminant = b**2 - 4*a*c

            root1 = (-b - np.sqrt(discriminant)) / (2*a)
            root2 = (-b + np.sqrt(discriminant)) / (2*a)

            # Determine the interval where the inequality holds
            valid_interval = (min(root1, root2), max(root1, root2))

            # Ensure the interval is within the constraints 0 <= x <= time
            lower_bound = max(0, valid_interval[0])
            upper_bound = min(time, valid_interval[1])

            min_x , max_x = np.ceil(lower_bound) , np.floor(upper_bound)

            return int(min_x) , int(max_x)

        res = 1
        for time , distance in self.input:
            min_x , max_x = find_interval(time, distance+1)
            res *= max_x - min_x + 1
        return res

    def part2(self):
        self.time = int(reduce(lambda acc , xs : acc + str(xs), self.time, ""))
        self.dist = int(reduce(lambda acc , xs : acc + str(xs), self.dist, ""))
        self.input = [(self.time, self.dist)]
        res = self.part1()

        return res