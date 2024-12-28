from day import Day

class Day17(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        parsed = {}
        self.rows = self.input.process_data_as_rows(0)
        for row in self.rows:
            parse = row.replace('Register', '').strip().split(':')
            key , val = parse[0] , parse[1]
            parsed[key] = int(val)
        self.rows = parsed
        self.program = self.input.process_data_as_rows(1)
        self.program = self.input.int_list(self.program[0].replace('Program:', '').strip().split(','))
        self.pointer = 0

    def literal_val(self, literal):
        return literal
    def combo_val(self, combo):
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
    def eval(self, opcode, operand):
        match opcode:
            case 0:
                numerator = self.rows['A']
                denominator = 2 ** self.combo_val(operand)
                self.rows['A'] = numerator // denominator
                self.pointer += 2
            case 1:
                self.rows['B'] = self.rows['B'] ^ self.literal_val(operand)
                self.pointer += 2
            case 2:
                self.rows['B'] = self.combo_val(operand) % 8
                self.pointer += 2
            case 3:
                if self.rows['A'] == 0:
                    self.pointer += 2
                else:
                    self.pointer = self.literal_val(operand)
            case 4:
                self.rows['B'] = self.rows['B'] ^ self.rows['C']
                self.pointer += 2
            case 5:
                val = self.combo_val(operand) % 8
                self.pointer += 2
                return str(val)
            case 6:
                numerator = self.rows['A']
                denominator = 2 ** self.combo_val(operand)
                self.rows['B'] = numerator // denominator
                self.pointer += 2
            case 7:
                numerator = self.rows['A']
                denominator = 2 ** self.combo_val(operand)
                self.rows['C'] = numerator // denominator
                self.pointer += 2
        return ""

    def eval_program(self):
        if self.pointer == len(self.program)-1:
            print("halt")
        ret = self.eval(self.program[self.pointer], self.program[self.pointer+1])
        if self.pointer == len(self.program):
            return ret
        else:
            return ret + self.eval_program()

    def part1(self):
        return ",".join(list(self.eval_program()))

    def part2(self):
        def reset_memory():
            self.rows['A'] = 0
            self.rows['B'] = 0
            self.rows['C'] = 0
            self.pointer = 0
        def eval_for(val):
            reset_memory()
            self.rows['A'] = val
            return self.input.int_list(self.eval_program())
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

        return get_min_A()
