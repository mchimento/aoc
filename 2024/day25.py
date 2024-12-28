from day import Day
import re
class Day25(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
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

        self.keys = []
        self.locks = []
        self.rows = self.input.process_data_as_string(0, "\n")
        print(self.rows)

        for schematic in re.split("\n\n", self.rows):
            scheme = re.split("\n", schematic)
            columns = [''.join(column) for column in zip(*scheme)]
            if scheme[0] == ('#' * len(scheme[0])):
                pins = get_pins(True, columns)
                self.keys.append(pins)
            else:
                pins = get_pins(False, columns)
                self.locks.append(pins)

    def part1(self):
        pairs = [ (x, y) for x in self.keys for y in self.locks ]
        join_p = [ list(zip(p[0],p[1])) for p in pairs ]
        length = len(self.keys[0])
        count = 0
        for xs in join_p:
            if all(val <= length for val in list(map(lambda p : p[0]+p[1] , xs))):
                count += 1
        return count

    def part2(self):
        return super().part2()