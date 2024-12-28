from day import Day
from functools import reduce
from collections import defaultdict

class Day05(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.check_rules = self.input.process_data_as_rows(0)
        self.updates = self.input.process_data_as_rows(1)
        self.updates = [ self.input.int_list(update.split(",")) for update in self.updates]
        self.check_rules = reduce(lambda acc, rule: {**acc, int(rule.split("|")[0]) : acc.get(int(rule.split("|")[0]), []) + [int(rule.split("|")[1])]}, self.check_rules, defaultdict(list))

    def part1(self):
        def val_is_sorted_forward(x, xs, ind):
            for i , val in enumerate(xs):
                if i <= ind:
                    continue
                if val == x:
                    continue
                if not x in self.check_rules:
                    return True
                ordering = self.check_rules[x]
                if val in ordering:
                    continue
                else:
                    return False
            return True
        def val_is_sorted_backwards(x, xs, ind):
            aux = [ val for val in xs[:ind] if x in self.check_rules and val in self.check_rules[x]]
            return not aux

        def val_is_sorted(x, xs, i):
            return val_is_sorted_forward(x, xs, i) and val_is_sorted_backwards(x, xs, i)

        def update_is_sorted(update):
            res = True
            for i , x in enumerate(update):
                res = res and val_is_sorted(x, update, i)
            return res

        def get_middle_value(xs):
            if not xs:
                return None
            if len(xs) % 2 == 1:
                return xs[len(xs) // 2]
            else:
                return xs[len(xs) // 2 - 1: len(xs) // 2 + 1]

        res = []
        for update in self.updates:
            if update_is_sorted(update):
                res.append(get_middle_value(update))
        res = self.input.int_list(res)
        return sum(res)

    def part2(self):
        def val_is_sorted_forward(x, xs, ind):
            for i , val in enumerate(xs):
                if i <= ind:
                    continue
                if val == x:
                    continue
                if not x in self.check_rules:
                    return True
                ordering = self.check_rules[x]
                if val in ordering:
                    continue
                else:
                    return False
            return True
        def val_is_sorted_backwards(x, xs, ind):
            aux = [ val for val in xs[:ind] if x in self.check_rules and val in self.check_rules[x]]
            return not aux

        def val_is_sorted(x, xs, i):
            return val_is_sorted_forward(x, xs, i) and val_is_sorted_backwards(x, xs, i)

        def update_is_sorted(xs):
            res = True
            for i , x in enumerate(xs):
                res = res and val_is_sorted(x, xs, i)
            return res

        def get_middle_value(xs):
            if not xs:
                return None
            if len(xs) % 2 == 1:
                return xs[len(xs) // 2]
            else:
                return xs[len(xs) // 2 - 1: len(xs) // 2 + 1]

        def sort_update(xs):
            res = []
            for _ , x in enumerate(xs):
                hits = [ y for y in xs if x in self.check_rules and y in self.check_rules[x] ]
                res.append((x, len(hits)))
            res = sorted(res, key=lambda x: x[1], reverse=True)
            return [x[0] for x in res]

        res = []
        for update in self.updates:
            if not update_is_sorted(update):
                res.append(get_middle_value(sort_update(update)))
        res = self.input.int_list(res)
        return sum(res)