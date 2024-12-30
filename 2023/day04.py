from day import Day
import re
from collections import defaultdict

class Day04(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_rows(0)
        self.scratch = []
        for line in input:
            card_id_str , card = line.split(":")
            card_id = int(card_id_str.split()[1])
            winners , own = card.split("|")
            winners = [ int(x) for x in re.findall(r'\d+', winners) ]
            own = [ int(x) for x in re.findall(r'\d+', own) ]
            numbers = {}
            numbers[card_id] = {'w' : winners, 'own' : own}
            self.scratch.append(numbers)

    def part1(self):
        total = 0
        for card in self.scratch:
            points = 0
            for _ , numbers in card.items():
                winner = numbers['w']
                own = numbers['own']
                for number in own:
                    if number in winner:
                        if points == 0:
                            points = 1
                        else:
                            points *= 2
                total += points

        return total

    def part2(self):
        total = 0
        copies = defaultdict(int)
        for card in self.scratch:
            points = 0
            for card_id, numbers in card.items():
                copies[card_id] += 1
                winner = numbers['w']
                own = numbers['own']
                for number in own:
                    if number in winner:
                        points += 1
                if points == 0:
                    continue
                for i in range(card_id + 1, card_id + points+1):
                    copies[i] += copies[card_id]

        for card_id, copies in copies.items():
            total += copies
        return total