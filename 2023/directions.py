class Directions:

    def __init__(self, wall = None, empty='.'):
        self.up = '^'
        self.down = 'v'
        self.left = '<'
        self.right = '>'
        self.directions = [self.up, self.down , self.left, self.right ]
        self.empty = empty
        self.wall = wall

    def coord(self, dir):
        match dir:
            case self.up:
                return (-1, 0)
            case self.down:
                return (1, 0)
            case self.right:
                return (0, 1)
            case self.left:
                return (0, -1)

    def turn_around(self, dir):
        return self.rotate90_clockwise(self.rotate90_clockwise(dir))

    def rotate90_clockwise(self, dir):
        if dir == self.right:
            return self.down
        elif dir == self.left:
            return self.up
        elif dir == self.up:
            return self.right
        elif dir == self.down:
            return self.left

    def rotate90_anticlockwise(self, dir):
        if dir == self.right:
            return self.up
        elif dir == self.left:
            return self.down
        elif dir == self.up:
            return self.left
        elif dir == self.down:
            return self.right
