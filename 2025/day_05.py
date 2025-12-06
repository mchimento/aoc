from day import Day

class Day5(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_blocks(0)
        def parse_range(id_range):
            return [int(x) for x in id_range.split('-')]

        self.id_ranges = [ parse_range(id_range) for id_range in input[0] ]
        self.ids = [ int(id) for id in input[1] ]

    def id_in_range(self, id, id_range):
        return id >= id_range[0] and id <= id_range[1]

    def range_cap(self, x1, y1, x2, y2):
        if x1 >= x2 and y1 <= y2:
            return []
        elif x1 >= x2 and y2 < y1:
            return [x1, y2]
        elif x1 < x2 and y1 <= y2 and y1 >= x2:
            return [x1, ]
        else:
            return [x1, y1]

    def range_cap(self, x1, y1, x2, y2):
        # no overlap
        if y1 < x2 or y2 < x1:
            return [(x1, y1)]
        # first range is completely inside second range
        if x1 >= x2 and y1 <= y2:
            return []
        # second range is completely inside first range
        if x1 < x2 and y1 > y2:
            return [(x1, x2-1), (y2+1, y1)]
        # second range overlaps on the right
        if x1 < x2 and y1 >= x2:
            return [(x1, x2-1)]
        # second range overlaps on the left
        if x1 <= y2 and y1 > y2:
            return [(y2+1, y1)]

        return []

    def part1(self):
        fresh = 0
        for id in self.ids:
            is_fresh = any(map(lambda id_range: self.id_in_range(id, id_range), self.id_ranges))
            if is_fresh:
                fresh += 1
        return fresh

    def part2(self):
        ids = 0
        for ix , (x , y) in enumerate(self.id_ranges):
            ranges = [[x,y]]
            for iy in range(ix+1, len(self.id_ranges)):
                nranges = []
                for r in ranges:
                    nranges += self.range_cap(r[0], r[1], self.id_ranges[iy][0], self.id_ranges[iy][1])
                ranges = nranges

            for nrange in ranges:
                ids += nrange[1] - nrange[0] + 1
        return ids