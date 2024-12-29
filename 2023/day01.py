from day import Day
import re

class Day01(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.calibration = self.input.process_data_as_rows(0)

    def part1(self):
        all_digits = []
        for calibration in self.calibration:
            digits = ''.join(re.findall(r'\d', calibration))
            all_digits.append(int(digits[0] + digits[-1]))

        return sum(all_digits)

    def part2(self):
        def convert(num):
            match num:
                case 'one': return 1
                case 'two': return 2
                case 'three': return 3
                case 'four': return 4
                case 'five': return 5
                case 'six': return 6
                case 'seven': return 7
                case 'eight': return 8
                case 'nine': return 9
                case _: return int(num)

        all_digits = []
        for calibration in self.calibration:
            digits = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', calibration)
            all_digits.append(convert(digits[0]) * 10 + convert(digits[-1]))

        return sum(all_digits)