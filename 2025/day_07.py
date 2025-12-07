from day import Day
from grid import Grid
from directions import Directions
from collections import Counter

class Day7(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.input = self.input.process_data_as_listed_rows(0)
        self.grid = Grid(self.input, Directions('^'))
        self.timelines = 1

    def part1(self):
        beams = Counter()
        start_pos = self.grid.get_elem_pos('S')
        beams[start_pos] = 1
        ret = 0
        for ix in range(0, self.grid.height()-1):
            beams_aux = Counter()
            for (x,y), count in beams.items():
                nx , ny , dir = self.grid.move_from(x, y, self.grid.dirs.down)
                if dir == self.grid.dirs.down:
                    beams_aux[(nx, ny)] += count
                else:
                    ret += 1
                    if self.grid.is_valid_coord(x+1, y-1):
                        beams_aux[(x+1, y-1)] += count
                    if self.grid.is_valid_coord(x+1, y+1):
                        beams_aux[(x+1, y+1)] += count
            beams = beams_aux

        self.timelines = sum(beams.values())
        return ret

    def part2(self):
        return self.timelines