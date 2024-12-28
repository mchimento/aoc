from day import Day

class Day09(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.int_grid(self.input.process_data_as_rows(0))[0]
        self.map = {}
        self.highest_id = 0

    def part1(self):
        def is_even(n):
            return n % 2 == 0
        def block_map():
            res = []
            id = 0
            for i , file in enumerate(self.rows):
                if is_even(i):
                    self.map[id] = file
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
        block_map()
        return check_sum()

    def part2(self):
        def get_id_index(id):
            for x in range(len(self.rows)):
                if self.rows[x] == id:
                    return x
            else:
                return None
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
                size = self.map[id]
                if size <= space:
                    back = get_id_index(id)
                    for y in range(size):
                        self.rows[i+y] = id
                        self.rows[back+y] = '.'
                    break
        res = 0
        for i , val in enumerate(self.rows):
            if  val == '.':
                continue
            res += i * val
        return res