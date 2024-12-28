import re
from collections import defaultdict
import time
from day24 import Day24
from day import Day

class AdventOfCode:

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

            binary = bin(to_int(self.out))[2:]
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
        #self.day = Day()
        #self.rows = self.day.input.process_data_as_rows(0)
        #self.rows = self.process_data_as_string(file_paths[0], "\n")
        #self.rows = [ list(row) for row in self.rows ]
        #self.columns = self.process_data_as_columns(file_paths[0])
        #day01.day1_part1(self.columns)
        day = Day24()
        day.run()
        #day.run_connected()
        #self.day18()

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()