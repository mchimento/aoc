import time
from day08 import Day08

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day08()
        #day.run(run_1=False, run_2=True)
        day.run()
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()