from day import Day
from collections import Counter

class Day11(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)
        self.rows = self.rows[0].split(" ")

    def count_stones(self, blinks):
        stones = self.input.int_list(self.rows)
        stone_counts = Counter(stones)
        for _ in range(blinks):
            new_counts = Counter()
            for stone, count in stone_counts.items():
                if stone == 0:
                    new_counts[1] += count
                elif len(str(stone)) % 2 == 0:
                    half_len = len(str(stone)) // 2
                    left = int(str(stone)[:half_len])
                    right = int(str(stone)[half_len:])
                    new_counts[left] += count
                    new_counts[right] += count
                else:
                    new_counts[stone * 2024] += count
            stone_counts = new_counts

        return sum(stone_counts.values())

    def part1(self):
        return self.count_stones(25)

    def part2(self):
        return self.count_stones(75)