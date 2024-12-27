from day import Day
import re

class Day03(Day):

    def __init__(self):
        self.data = []
        super().__init__()

    def parse_input(self):
        self.data = self.input.process_data_as_string(0)

    def part1(self):
        pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
        matches = re.findall(pattern, self.data)
        results = sum([int(num1) * int(num2) for num1, num2 in matches])
        return results

    def part2(self):
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
        def evaluate_multiplications(expr_list):
            results = []
            for expr in expr_list:
                numbers = list(map(int, expr.replace('mul(', '').replace(')', '').split(',')))
                results.append(numbers[0] * numbers[1])

            return results
        return sum(evaluate_multiplications(eval(matches, True)))