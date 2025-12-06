from day import Day
from grid import Grid

class Day4(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_listed_rows(0)
        self.grid = Grid(input)
        #self.grid.print_grid()


    def remove_rolls(self):
        rolls = []
        for x in range(0, self.grid.width()):
            for y in range(0, self.grid.height()):
                if self.grid[x, y] == '@':
                    reach = self.grid.get_adjacent(x, y, filter_func=lambda x , y: self.grid[x, y] == '@')
                    if len(reach) < 4:
                        rolls.append((x, y))
        self.grid.fill_grid(rolls, 'X')
        return len(rolls)

    def part1(self):
        rolls = self.remove_rolls()
        return rolls

    def part2(self):
        removed = self.remove_rolls()
        rolls = removed
        
        while removed != 0:
            removed = self.remove_rolls()
            rolls += removed

        #print(rolls)
        #self.grid.fill_grid(rolls, 'X')
        #self.grid.print_grid()
        return rolls