import time
from day07 import Day07

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day07()
        #day.run(run_1=False, run_2=True)
        day.run()
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()