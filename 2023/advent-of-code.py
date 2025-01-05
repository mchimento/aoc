import time
from day12 import Day12

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day12()
        #day.run(run_1=False, run_2=True)
        day.run()
        #day.run_connected()
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()