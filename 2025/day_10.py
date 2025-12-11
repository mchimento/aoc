from day import Day
import re
from itertools import combinations
from ortools.linear_solver import pywraplp
import numpy as np

class Day10(Day):

    def __init__(self):
        super().__init__()

    def parse_line(self, s):
        s = s.strip()

        square = re.search(r"\[(.*?)\]", s).group(1).strip()

        parens_raw = re.findall(r"\((.*?)\)", s)
        parens = []
        for item in parens_raw:
            if "," in item:
                parens.append(self.button_to_bits(list(map(int, item.split(","))), len(square)))
            else:
                parens.append(self.button_to_bits([int(item)], len(square)))

        braces_raw = re.search(r"\{(.*?)\}", s).group(1)
        braces = list(map(int, braces_raw.split(",")))
        return [self.machine_to_bin(list(square)), parens, braces]

    def machine_to_bin(self, machine):
        return ''.join('1' if c == '#' else '0' for c in machine)

    def button_to_bits(self, indices, n):
        bits = ['0'] * n
        for i in indices:
            bits[i] = '1'
        return ''.join(bits)

    def xor(self, a, b):
        """Press button"""
        n = len(a)
        ai = int(a, 2)
        bi = int(b, 2)
        return format(ai ^ bi, f'0{n}b')

    def parse_input(self):
        self.input = self.input.process_data_as_rows(0)
        self.input = list(map(lambda s: self.parse_line(s), self.input))

    def find_buttons_to_press(self, machine, buttons):
        n = len(machine)
        target = int(machine, 2)
        buttons_int = [int(b, 2) for b in buttons]

        best_solution = None

        def dfs(current_xor, index, pressed):
            nonlocal best_solution

            if best_solution is not None and len(pressed) >= len(best_solution):
                return
            if current_xor == target:
                best_solution = pressed.copy()
                return
            if index >= len(buttons_int):
                return
            # press button
            dfs(current_xor ^ buttons_int[index], index + 1, pressed + [index])
            # skip button
            dfs(current_xor, index + 1, pressed)

        dfs(0, 0, [])

        if best_solution is None:
            return None

        return best_solution

    def solve_repeated_presses(self, target, buttons):
        n_pos = len(target)
        n_btn = len(buttons)

        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise Exception("Solver not available")

        # Integer variables: number of times each button is pressed
        x = [solver.IntVar(0, solver.infinity(), f'x{i}') for i in range(n_btn)]

        # Constraints: sum of button effects = target counts
        for pos in range(n_pos):
            constraint = solver.Sum([x[btn] * buttons[btn][pos] for btn in range(n_btn)]) == target[pos]
            solver.Add(constraint)

        solver.Minimize(solver.Sum(x))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return int(solver.Objective().Value())
        else:
            return None  # no solution

    def part1(self):
        ret = 0
        for row in self.input:
            machine, buttons, joltage = row[0], row[1], row[2]
            solution = self.find_buttons_to_press(machine, buttons)
            ret += len(solution)

        return ret

    def part2(self):
        total_presses = 0
        for machine, buttons, joltage in self.input:
            buttons_int = [[int(c) for c in b] for b in buttons]
            res = self.solve_repeated_presses(joltage, buttons_int)
            if res is None:
                raise RuntimeError("No valid solution for target:", joltage)
            total_presses += res
        return total_presses
