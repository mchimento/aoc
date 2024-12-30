from day import Day
import re

class Day05(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.seeds = self.input.process_data_as_string(0)
        self.seeds = list(map(int, self.seeds.split(":")[1].strip().split(" ")))
        self.maps = []
        for block in self.input.process_data_as_blocks(1):
            block.pop(0)
            block = [ list(map(int, xs.split(" "))) for xs in block]
            self.maps.append(block)

    def seed_in_map(self, seed, block):
        _ , source, size = block
        if source <= seed <= source + size - 1:
            return True
        else:
            return False

    def part1(self):
        min_loc = 0
        for seed in self.seeds:
            print(f"Seed: {seed}")
            current = seed
            for blocks in self.maps:
                for block in blocks:
                    if self.seed_in_map(current, block):
                        current = block[0] + current - block[1]
                        print(f"Block: {block}")
                        print(f"Map to: {current}")
                        break
                print(f"Stayed at: {current}")
            if current < min_loc:
                min_loc = current
            elif min_loc == 0:
                min_loc = current
        return min_loc

    def part2(self):
        def check_seeds_range(seed, range, block):
            dest , source, size = block
            start_range , end_range = seed , seed + range
            start_block , end_block = source , source + size

            if start_range > end_block or end_range < start_block:
                return (seed, range) , []
            max_lb = max(start_range, start_block)
            min_ub = min(end_range, end_block)

            difference_ranges = []
            if start_range < start_block:
                difference_ranges.append((start_range, start_block - start_range))

            if end_range > end_block:
                difference_ranges.append((end_block, end_range - end_block))

            if max_lb == start_block:
                new_source = dest
            else:
                new_source = dest + start_range - start_block

            return (new_source, min_ub - max_lb) , difference_ranges

        seed_ranges = []
        for i in range(0, len(self.seeds), 2):
            seed_ranges.append((self.seeds[i], self.seeds[i+1]))

        def check_seed(seed, block):
            seed, range_ = seed
            new_seed_range , difference_ranges = check_seeds_range(seed, range_, block)
            if difference_ranges:
                return new_seed_range , difference_ranges , False
            else:
                return new_seed_range , [] , new_seed_range == (seed, range_)

        def check_seeds(seeds, block):
            new_ranges = []
            out_of_block = []
            for seed in seeds:
                new_seed_range , difference_ranges , is_same = check_seed(seed, block)
                if difference_ranges:
                    out_of_block += difference_ranges
                    new_ranges.append(new_seed_range)
                else:
                    if is_same:
                        out_of_block.append(new_seed_range)
                    else:
                        new_ranges.append(new_seed_range)
            return new_ranges , out_of_block

        locs = []
        for seed_range in seed_ranges:
            check_ranges = [seed_range]
            for blocks in self.maps:
                current = check_ranges
                check_ranges = []
                for block in blocks:
                    new_ranges , out_of_block = check_seeds(current, block)
                    if not out_of_block:
                        check_ranges += new_ranges
                        break
                    else:
                        current = out_of_block
                        check_ranges += new_ranges
                if not check_ranges:
                    check_ranges = out_of_block

            locs += new_ranges + out_of_block

        return sorted(locs)[0][0]