from day import Day

class Day2(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        input = self.input.process_data_as_string(0).split(',')
        parse = [ x.split('-') for x in input ]
        self.input = [ (int(x[0]), int(x[1])) for x in parse ]

    def is_valid_id1(self, id):
        id_str = str(id)
        half1 = id_str[:len(id_str) // 2] 
        half2 = id_str[len(id_str) // 2:]

        return half1 == half2 

    def is_valid_id2(self, id):
        id_str = str(id)
        multiplos = [ x for x in range(1, len(id_str)) if len(id_str) % x == 0 ]
        is_valid = False
        
        def all_same(xs):
            return len(set(xs)) <= 1

        for x in multiplos:
            chunks = [id_str[i:i+x] for i in range(0, len(id_str), x)]
            is_valid = is_valid or all_same(chunks)            
        
        return is_valid

    def part1(self):
        ret = 0
        for (x, y) in self.input:
           xs = [ val for val in range(x, y+1) if self.is_valid_id1(val) ]
           ret += sum(xs)

        return ret

    def part2(self):
        ret = 0
        for (x, y) in self.input:
           xs = [ val for val in range(x, y+1) if self.is_valid_id2(val) ]
           ret += sum(xs)
        
        return ret