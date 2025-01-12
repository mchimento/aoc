from day import Day

class Day13(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.blocks = self.input.process_data_as_blocks(0)

    def num_of_diff(self, line1, line2, diff):
        d = 0
        for a, b in zip(line1, line2):
            if a != b: d += 1
            if d > diff: break
        return d

    def find_mirror(self, block, diff=0):
        for r in range(len(block)-1):
            d = 0
            for i in range(min(r+1, len(block)-r-1)):
                d += self.num_of_diff(block[r-i], block[r+1+i], diff)
                if d > diff: break
            else:
                if d == diff:
                    return r+1, 0
        return self.find_mirror(list(zip(*block)), diff)[::-1]

    def summarize(self, diff=0):
        res = 0
        for block in self.blocks:
            r, c = self.find_mirror(block, diff)
            res += c+100*r
        return res

    def part1(self):
        return self.summarize(0)

    def part2(self):
        return self.summarize(1)