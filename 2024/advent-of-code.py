import time
from day25 import Day25

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day25()
        day.run(True)
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()