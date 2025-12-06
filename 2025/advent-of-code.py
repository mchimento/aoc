import time
from day_01 import Day1
from day_02 import Day2
from day_03 import Day3

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day3()
        day.run(True)
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()