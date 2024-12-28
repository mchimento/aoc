from day import Day

class Day10(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.int_grid(self.input.process_data_as_rows(0))
        self.trailheads = []
        for x in range(0, len(self.rows)):
            for y in range(0, len(self.rows[0])):
                if self.rows[x][y] == 0:
                    self.trailheads.append((x, y))

    def reachable_coords(self, x, y, val):
        reachables = []
        if 0 <= x - 1  < len(self.rows):
            if self.rows[x-1][y] == val:
                reachables.append((x-1, y))
        if 0 <= x + 1  < len(self.rows):
            if self.rows[x+1][y] == val:
                reachables.append((x+1, y))
        if 0 <= y - 1  < len(self.rows[0]):
            if self.rows[x][y-1] == val:
                reachables.append((x, y-1))
        if 0 <= y + 1  < len(self.rows[0]):
            if self.rows[x][y+1] == val:
                reachables.append((x, y+1))
        return reachables

    def check_trailhead(self, trailhead):
        paths = [[(trailhead[0], trailhead[1])]]
        for val in range(1, 10):
            new_paths = []
            for path in paths:
                x , y = path[len(path)-1]
                next_positions = self.reachable_coords(x, y, val)
                if not next_positions:
                    continue
                for pos in next_positions:
                    new_path = path.copy()
                    new_path.append(pos)
                    new_paths.append(new_path)
            paths = new_paths
        return paths

    def part1(self):
        def trials_score(trials):
            reached = set()
            for trial in trials:
                reached.add(trial[len(trial)-1])
            return len(reached)
        res = 0
        for trailhead in self.trailheads:
            res += trials_score(self.check_trailhead(trailhead))
        return res

    def part2(self):
        res = 0
        for trailhead in self.trailheads:
            res += len(self.check_trailhead(trailhead))
        return res