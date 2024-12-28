from day import Day
import re
from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD
from sympy import solve, Symbol

class Day13(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_string(0)
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

        self.problems = []
        for i in range(0, len(parsed_elements), 3):
            problem = [parsed_elements[i], parsed_elements[i+1], parsed_elements[i+2]]
            self.problems.append(problem)

    def part1(self):
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

        return find_tokens(self.problems)

    def part2(self):
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

        def find_tokens_unbound(nlp):
            final = 0
            for problem in nlp:
                A = problem[0]
                B = problem[1]
                X = problem[2]
                final += solve_lp_int_numpy(A[2], A[4], B[2], B[4], X[1], X[3])
            return final

        return find_tokens_unbound(self.problems)