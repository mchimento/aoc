from day import Day
import re

class Day24(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)
        self.variables = {}
        self.x = {}
        self.y = {}
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
        self.gates = self.input.process_data_as_rows(1)
        for gate in self.gates:
            match = re.match(regex, gate)
            if match:
                exps = list(match.groups())
                parsed_gates.append(exps)
        self.gates = parsed_gates

        self.out = {}
        self.context = {}
        self.var_vals = {}

    def to_int(self, num):
            binary = ""
            for value in sorted(num, reverse=True):
                binary += str(num[value])
            return int(binary, 2)

    def part1(self):
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

        eval_gates()
        return self.to_int(self.out)

    def part2(self):
        preserve = set()
        swap_candidates = set()
        z = self.to_int(self.x) + self.to_int(self.y)
        z_bin = list(str(bin(z)[2:]))[::-1]
        expected_out = {}
        for i in range(len(z_bin)):
            if i <= 9:
                key = f"z0{i}"
            else:
                key = f"z{i}"
            expected_out[key] = z_bin[i]
        e_int = self.to_int(expected_out)
        e_bin = bin(e_int)[2:]

        binary = bin(self.to_int(self.out))[2:]
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