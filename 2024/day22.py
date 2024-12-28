from day import Day

class Day22(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.secrets = {}
        self.rows = self.input.process_data_as_rows(0)
        id = 0
        for row in self.rows:
            self.secrets[id] = [int(row)]
            id += 1
        self.prices = {}
        self.max_price = {}
        self.variations = {}
        self.sum_secrets = 0
        self.seqs = {}
        self.max_seq = None

    def part1(self):
        def new_secret(secret):
            step1 = ((secret * 64) ^ secret) % 16777216
            step2 = ((step1 // 32) ^ step1) % 16777216
            step3 = ((step2 * 2048) ^ step2) % 16777216
            return step3
        def get_buyers_secrets(amount):
            last_secret = None
            for i in range(amount):
                for id , secrets in self.secrets.items():
                    last_secret = new_secret(secrets[-1])
                    price = last_secret % 10
                    if i == 0:
                        self.secrets[id] = [last_secret]
                        self.prices[id] = [price]
                        self.max_price[id] = price
                    else:
                        self.secrets[id].append(last_secret)
                        self.prices[id].append(price)
                        self.max_price[id] = price if self.max_price[id] < price else self.max_price[id]
                    if i == amount -1:
                        vars_and_max(self.prices[id], id)
                        self.sum_secrets += last_secret
        def vars_and_max(prices, id):
            vars = []
            prev = 0
            visited = set()
            for i , price in enumerate(prices):
                if i == 0:
                    vars.append(0)
                    prev = price
                    continue
                vars.append(price - prev)
                prev = price
                if i >= 4:
                    seq = tuple(vars[i-3:i+1])
                    if seq in visited:
                        continue
                    else:
                        visited.add(seq)
                    if seq in self.seqs:
                        self.seqs[seq]['price'] += price
                        self.seqs[seq]['touches_max'] = self.seqs[seq]['touches_max'] or (price == self.max_price[id])
                    else:
                        self.seqs[seq] = {}
                        self.seqs[seq]['price'] = price
                        self.seqs[seq]['touches_max'] = price == self.max_price[id]
                    new_price = self.seqs[seq]['price']
                    is_max = self.seqs[seq]['touches_max']
                    if self.max_seq is None and is_max:
                        self.max_seq = seq , price
                    elif self.max_seq is None:
                        continue
                    else:
                        _ , maxp_m = self.max_seq
                        if maxp_m < new_price and is_max:
                            self.max_seq = seq , new_price
            return vars

        get_buyers_secrets(2000)
        return self.sum_secrets

    def part2(self):
        return self.max_seq[1]