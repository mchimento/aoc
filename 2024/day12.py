from day import Day

class Day12(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.rows_listed(self.input.process_data_as_rows(0))
        self.regions = self.getRegions()

    def check_plot_after(self, x, y, plant):
        if y + 1 < len(self.rows[0]):
            return plant == self.rows[x][y+1]
        else:
            return False
    def check_plot_before(self, x, y, plant):
        if y - 1 >= 0:
            return plant == self.rows[x][y-1]
        else:
            return False
    def check_plot_below(self, x, y, plant):
        if x + 1 < len(self.rows):
            return plant == self.rows[x+1][y]
        else:
            return False
    def check_plot_above(self, x, y, plant):
        if x - 1 >= 0:
            return plant == self.rows[x-1][y]
        else:
            return False
    def check_area(self, x, y, plant):
        self.rows[x][y] = None
        analyse = [(x,y)]
        region = [(x,y)]
        while(analyse != []):
            x , y = analyse.pop(0)
            if self.check_plot_after(x, y, plant):
                region.append((x,y+1))
                analyse.append((x,y+1))
                self.rows[x][y+1] = None
            if self.check_plot_before(x, y, plant):
                region.append((x,y-1))
                analyse.append((x,y-1))
                self.rows[x][y-1] = None
            if self.check_plot_below(x, y, plant):
                region.append((x+1,y))
                analyse.append((x+1,y))
                self.rows[x+1][y] = None
            if self.check_plot_above(x, y, plant):
                region.append((x-1,y))
                analyse.append((x-1,y))
                self.rows[x-1][y] = None
        return region

    def getRegions(self):
        regions = []
        plant = None
        for x in range(0, len(self.rows)):
            for y in range(0, len(self.rows[0])):
                if self.rows[x][y] is None:
                    continue
                plant = self.rows[x][y]
                area = self.check_area(x, y, plant)
                regions.append((area, plant))
        return regions

    def part1(self):
        def perimeter(region):
            total = 4 * len(region)
            for (x , y) in region:
                if (x, y+1) in region:
                    total -= 1
                if (x+1, y) in region:
                    total -= 1
                if (x, y-1) in region:
                    total -= 1
                if (x-1, y) in region:
                    total -= 1
            return total
        res = 0
        for region in self.regions:
            res += len(region[0]) * perimeter(region[0])
        return res

    def part2(self):
        def sides(region):
            sides = 0
            for (x, y) in region:
                left , right , above , below = x - 1 , x + 1, y - 1, y + 1
                right_not_in_region = (right, y) not in region
                below_not_region = (x, below) not in region

                if (x, above) not in region:
                    if right_not_in_region or (right, above) in region:
                        sides += 1
                if (x, below) not in region:
                    if right_not_in_region or (right, below) in region:
                        sides += 1
                if (left, y) not in region:
                    if below_not_region or (left, below) in region:
                        sides += 1
                if (right, y) not in region:
                    if below_not_region or (right, below) in region:
                        sides += 1
            return sides
        res = 0
        for region in self.regions:
            res += len(region[0]) * sides(region[0])
        return res