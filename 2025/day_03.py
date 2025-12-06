from day import Day

class Day3(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.input = self.input.process_data_as_listed_rows(0)
        print(input)
        return

    def get_two_highest(self, bank):
        fst = int(bank[0])
        snd = int(bank[1])

        for ix , x_str in enumerate(bank[2:]):
            x = int(x_str)
            if x > snd and x > fst:
                if ix != len(bank[2:]) -1:
                    fst = x
                    snd = 0
                else:
                    fst = max(fst, snd)
                    snd = x
            elif x > fst:
                fst = snd
                snd = x
            elif x > snd:
                snd = x
        return fst*10 + snd

    def first_not_descending(self, xs):
        """Return index of first element that breaks descending order, or -1 if none."""
        for i in range(len(xs) - 1):
            if xs[i] < xs[i + 1]:
                return i+1
        return -1

    def get_n_highest(self, bank, n):
        joltage = [ int(x) for x in bank[:n] ]

        for ix in range(n, len(bank)):
            j_ix = self.first_not_descending(joltage)
            val = int(bank[ix])
            if j_ix >= 0:
                xs = joltage[:j_ix+1]
                smallest = min(xs)
                smallest_ix = xs.index(smallest)
                
                joltage.pop(smallest_ix)
                joltage.append(val)
            else:
                if joltage[-1] < val:
                    joltage.pop(-1)
                    joltage.append(val)

        return int(''.join(map(str, joltage)))

    def part1(self):
        joltage = 0
        for bank in self.input:
            tmp = self.get_two_highest(bank)
            joltage += self.get_two_highest(bank)
        return joltage

    def part2(self):        
        joltage = 0
        for bank in self.input:
            tmp = self.get_n_highest(bank, 12)
            joltage += self.get_n_highest(bank, 12)
        return joltage