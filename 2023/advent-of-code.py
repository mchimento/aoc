import time
from day01 import Day01

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day01()
        day.run(True)
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()