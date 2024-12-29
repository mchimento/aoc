from day import Day
import re

class Day02(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_rows(0)
        self.games = {}
        for row in input:
            game , sets = row.split(":")
            game_id = re.findall(r'\d+', game)[0]
            all_games = []
            for line in sets.strip().split(";"):
                game_sets = {}
                all_sets = line.split(",")
                for set_ in all_sets:
                    set_number, set_score = set_.split()
                    game_sets[set_score] = int(set_number)
                    all_games.append(game_sets)

            self.games[int(game_id)] = all_games

    def part1(self):
        def check_game_sets(games_sets, red, green, blue):
            for set in games_sets:
                if ('red' in set and set['red'] > red) or \
                    ('green' in set and set['green'] > green) or \
                    ('blue' in set and set['blue'] > blue):
                    return False
            return True
        res = 0
        for game , all_sets in self.games.items():
            if check_game_sets(all_sets, 12, 13, 14):
                res += game

        return res

    def part2(self):
        def check_min_game_sets(games_sets):
            red = 0
            green = 0
            blue = 0
            for set in games_sets:
                if 'red' in set:
                    red = max(red, set['red'])
                if 'green' in set:
                    green = max(green, set['green'])
                if 'blue' in set:
                    blue = max(blue, set['blue'])

            return red * green * blue
        res = 0
        for _ , all_sets in self.games.items():
            res += check_min_game_sets(all_sets)

        return res