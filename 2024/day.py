from input import Input

class Day:
    def __init__(self):
        self.input = Input()
        self.parse_input()

    def parse_input(self):
        return

    def run(self, only1=False):
        res1 = self.part1()
        print(f"Part 1: {res1}")
        if not only1:
            res2 = self.part2()
            print(f"Part 2: {res2}")

    def run_connected(self):
        res1 , args_part2 = self.part1()
        print(f"Part 1: {res1}")
        res2 = self.part2(args_part2)
        print(f"Part 2: {res2}")

    def part1(self):
        return 0

    def part2(self, args=None):
        return 0

    def print_to_file(self, s, file_path="output.txt", type='a'):
        with open(file_path, type) as file:
            print(s, file=file)