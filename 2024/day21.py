from day import Day
from directions import Directions
from collections import defaultdict
from functools import reduce

class Day21(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.codes = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.num_pad = [['7', '8', '9'], ['4', '5','6'],['1', '2', '3'], ['X', '0', 'A']]
        self.mapping_numpad = {
            '7' : (0,0), '8' : (0,1), '9' : (0,2),
            '4' : (1,0), '5' : (1,1), '6' : (1,2),
            '1' : (2,0), '2' : (2,1), '3' : (2,2),
            'X' : (3,0), '0' : (3,1), 'A' : (3,2)
        }
        self.num_pad_dirs = Directions(self.num_pad, wall='X')
        self.robot_pad = [['X', self.num_pad_dirs.up, 'A'], [self.num_pad_dirs.left, self.num_pad_dirs.down, self.num_pad_dirs.right]]
        self.robot_pad_dirs = Directions(self.robot_pad, wall='X')
        self.mapping_robotpad = {
            'X' : (0,0), self.robot_pad_dirs.up : (0,1), 'A' : (0,2),
            self.robot_pad_dirs.left : (1,0), self.robot_pad_dirs.down : (1,1), self.robot_pad_dirs.right : (1,2)
        }

    def shortest_path(self, key1, key2, pad, gap):
        r1, c1 = pad[key1]
        r2, c2 = pad[key2]
        # Vertical and horizontal movements
        ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
        lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

        # Safe to move vertically first if heading right and corner point isn't the gap
        if c2 > c1 and f"{r2},{c1}" != f"{gap[0]},{gap[1]}":
            return f"{ud}{lr}A"
        # Safe to move horizontally first if corner point isn't the gap
        if f"{r1},{c2}" != f"{gap[0]},{gap[1]}":
            return f"{lr}{ud}A"
        # Must move vertically first because we can't be in the same column as the gap
        return f"{ud}{lr}A"

    def sequences(self, seq, pad, gap):
        keys = []
        prev_key = "A"
        for key in seq:
            keys.append(self.shortest_path(prev_key, key, pad, gap))
            prev_key = key
        return keys

    def add_to_freq_table(self, f_table, sequence):
        f_table[sequence] = f_table.get(sequence, 0) + 1
        return f_table

    def seq_counts(self, sequence, pad, gap):
        subsequences = self.sequences(sequence, pad, gap)
        return reduce(self.add_to_freq_table, subsequences, defaultdict(int))

    def complexity_code(self, code, num_dir_robots=25):
        f_tables = [ {''.join(self.sequences(code, self.mapping_numpad, (3,0))) : 1}]

        for _ in range(num_dir_robots):
            new_f_tables = []
            for f_table in f_tables:
                new_dic = {}
                for seq, freq in f_table.items():
                    for sub_seq, sub_freq in self.seq_counts(seq, self.mapping_robotpad, (0, 0)).items():
                        new_dic[sub_seq] = new_dic.get(sub_seq, 0) + sub_freq * freq
                new_f_tables.append(new_dic)
            f_tables = new_f_tables

        def cmplx(freq_table):
            return sum(len(seq) * freq for seq, freq in freq_table.items())

        num = int("".join(code[:-1]))
        return sum(cmplx(f_table) * num for f_table in f_tables)

    def complexities(self, limit=25):
        ret = 0
        for code in self.codes:
            ret += self.complexity_code(code, limit)
        return ret

    def part1(self):
        return self.complexities(2)

    def part2(self):
        return self.complexities(25)