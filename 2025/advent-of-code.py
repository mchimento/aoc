import time
from day_01 import Day1
from day_02 import Day2
from day_03 import Day3
from day_04 import Day4

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day4()
        day.run(run_1=False)
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()