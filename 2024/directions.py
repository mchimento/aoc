class Directions:
    def __init__(self, grid, wall = None, empty='.'):
        self.up = '^'
        self.down = 'v'
        self.left = '<'
        self.right = '>'
        self.directions = [self.up, self.down , self.left, self.right ]
        self.empty = empty
        self.wall = wall
        self.grid = grid

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

    def move_from(self, x , y, dir):
        """
        Move from position (x, y) one step in the direction dir,
        unless the step is blocked by wall or we are the grid border
        """
        if dir == self.up:
            if x == 0:
                return x , y , self.rotate90_clockwise(dir)
            if self.wall is not None and self.grid[x-1][y] == self.wall:
                return x , y, self.rotate90_clockwise(dir)
            else:
                return x-1 , y, dir
        elif dir == self.down:
            if x == len(self.grid)-1:
                return x , y, self.rotate90_clockwise(dir)
            if self.wall is not None and self.grid[x+1][y] == self.wall:
                return x , y, self.rotate90_clockwise(dir)
            else:
                return x+1 , y , dir
        elif dir == self.right:
            if y == len(self.grid[0])-1:
                return x , y, self.rotate90_clockwise(dir)
            if self.wall is not None and self.grid[x][y+1] == self.wall:
                return x , y, self.rotate90_clockwise(dir)
            else:
                return x , y+1, dir
        elif dir == self.left:
            if y == 0:
                return x , y, self.rotate90_clockwise(dir)
            if self.wall is not None and self.grid[x][y-1] == self.wall:
                return x , y, self.rotate90_clockwise(dir)
            else:
                return x , y-1, dir
        else:
            return None
