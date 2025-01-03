from day import Day
from grid import Grid
from directions import Directions
from collections import deque

class Day10(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_listed_rows(0)
        self.dirs = Directions()
        self.pipes = Grid(input, self.dirs)

    def part1(self):
        def next_step(node, visited):
            x , y = node
            pipe = self.pipes[x, y]
            if self.pipes.is_valid_coord(x-1, y) and (x-1 , y) not in visited:
                match pipe , self.pipes[x-1, y]:
                    case '|', '7': return x-1, y
                    case '|', 'F': return x-1, y
                    case '|', '|': return x-1, y
                    case 'L', '|': return x-1, y
                    case 'J', '|': return x-1, y
                    case 'L', 'F': return x-1, y
                    case 'J', '7': return x-1, y
                    case 'J', 'F': return x-1, y
                    case 'L', '7': return x-1, y
                    case _ , _ : pass
            if self.pipes.is_valid_coord(x+1, y) and (x+1 , y) not in visited:
                match pipe , self.pipes[x+1, y]:
                    case '|', 'J': return x+1, y
                    case '|', 'L': return x+1, y
                    case '|', '|': return x+1, y
                    case '7', '|': return x+1, y
                    case 'F', '|': return x+1, y
                    case 'F', 'L': return x+1, y
                    case '7', 'J': return x+1, y
                    case 'F', 'J': return x+1, y
                    case '7', 'L': return x+1, y
                    case _ , _ : pass
            if self.pipes.is_valid_coord(x, y-1) and (x , y-1) not in visited:
                match pipe , self.pipes[x, y-1]:
                    case '-', 'F': return x, y-1
                    case '-', 'L': return x, y-1
                    case '-', '-': return x, y-1
                    case '7', '-': return x, y-1
                    case 'J', '-': return x, y-1
                    case 'J', 'L': return x, y-1
                    case '7', 'F': return x, y-1
                    case '7', 'L': return x, y-1
                    case 'J', 'F': return x, y-1
                    case _ , _ : pass
            if self.pipes.is_valid_coord(x, y+1) and (x , y+1) not in visited:
                match pipe , self.pipes[x, y+1]:
                    case '-', '7': return x, y+1
                    case '-', 'J': return x, y+1
                    case 'F', '-': return x, y+1
                    case 'L', '-': return x, y+1
                    case '-', '-': return x, y+1
                    case 'L', 'J': return x, y+1
                    case 'L', '7': return x, y+1
                    case 'F', '7': return x, y+1
                    case 'F', 'J': return x, y+1
                    case _ , _ : pass

            return x , y

        def get_start_nodes(start):
            x , y = start
            dirs = []
            if self.pipes.is_valid_coord(x, y-1):
                match self.pipes[x, y-1]:
                    case '-': dirs.append((x, y-1))
                    case 'F': dirs.append((x, y-1))
                    case 'L': dirs.append((x, y-1))
                    case _: pass
            if self.pipes.is_valid_coord(x, y+1):
                match self.pipes[x, y+1]:
                    case '-': dirs.append((x, y+1))
                    case '7': dirs.append((x, y+1))
                    case 'J': dirs.append((x, y+1))
                    case _: pass
            if self.pipes.is_valid_coord(x-1, y):
                match self.pipes[x-1, y]:
                    case 'F': dirs.append((x-1, y))
                    case '7': dirs.append((x-1, y))
                    case '|': dirs.append((x-1, y))
                    case _: pass
            if self.pipes.is_valid_coord(x+1, y):
                match self.pipes[x+1, y]:
                    case 'L': dirs.append((x+1, y))
                    case 'J': dirs.append((x+1, y))
                    case '|': dirs.append((x+1, y))
                    case _: pass

            return dirs[0] , dirs[1]

        start = self.pipes.get_elem_pos('S')
        node1 , node2 = get_start_nodes(start)
        path1 = []
        path2 = []
        current_node1 = node1
        current_node2 = node2

        while current_node1 != current_node2:
            path1.append(current_node1)
            path2.append(current_node2)
            current_node2 = next_step(current_node2, path2)
            current_node1 = next_step(current_node1, path1)
        path1.append(current_node1)
        path2.append(current_node2)
        path1.pop()

        return len(path2) , [[start] + path1 + path2[::-1]]

    def part2(self, args):
        # remove junk
        loop_path = args[0]
        for x in range(self.pipes.height()):
            for y in range(self.pipes.width()):
                if not (x,y) in loop_path:
                    self.pipes[x, y] = '.'

        # flood fill
        inside = self.pipes.find_enclosed_nodes_within_closed_path(loop_path)
        self.pipes.fill_grid(inside, 'I')

        return len(inside)