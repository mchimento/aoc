import time
from day13 import Day13

class AdventOfCode:

    def main(self):
        start = time.time()
        day = Day13()
        #day.run(run_1=False, run_2=True)
        day.run()
        #day.run_connected()
        end = time.time()
        print(f"Execution time: {end - start} seconds")

if __name__ == "__main__":
    main = AdventOfCode()
    main.main()