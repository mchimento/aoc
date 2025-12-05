from day import Day

class Day1(Day):

    def __init__(self):
        super().__init__()
        self.limit = 100

    def parse_input(self):
        self.input = [ (x[0], int(x[1:])) for x in self.input.process_data_as_rows(0)]

    def rotate(self, dir, amount, total):
        if dir == 'L':
            new = (total - amount) % self.limit
        else:
            new = (total + amount) % self.limit            
        return new

    def rotate_part2(self, dir, amount, total):
        rotations = 0
        if dir == 'R':
            rotations = (total + amount) // self.limit
            new_state = (total + amount) % self.limit
        else:
            new_state = (total - amount) % self.limit
            if total == 0:
                rotations = amount // self.limit
            elif amount > total:
                rotations = ((amount - total - 1) // self.limit) + 1
            if new_state == 0:
                rotations += 1
        return new_state, rotations

    def part1(self):        
        state = 50
        count = 0
        for (dir, val) in self.input:
            state = self.rotate(dir, val, state)
            if state == 0: 
                count += 1
        return count

    def part2(self):
        state = 50
        count = 0
        for (dir, val) in self.input:
            state, rotations = self.rotate_part2(dir, val, state)
            count += rotations 
        return count