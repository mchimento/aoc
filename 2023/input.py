import argparse

class Input:

    def __init__(self):
        self.file_paths = self.read_files()

    def read_files(self):
        """
        Main function to read command-line arguments and handle the file input.
        """
        parser = argparse.ArgumentParser(description="Process a file.")
        parser.add_argument("file_paths", nargs="+", type=str, help="Path to the input file")

        args = parser.parse_args()
        return args.file_paths

    def process_data_as_columns(self, file_ix):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                data = file.read().strip()
            rows = data.splitlines()
            columns = [''.join(column) for column in zip(*rows)]
            return columns
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def process_data_as_rows(self, file_ix):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                data = file.read().strip()
            return data.splitlines()
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def process_data_as_string(self, file_ix, eof_by=""):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                data = file.read().strip().replace("\n",eof_by)
            return data
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def int_list(self, list_string):
        return [ int(x) for x in list_string ]

    def rows_listed(self, rows):
        return [ list(row) for row in rows ]

    def int_grid(self, grid):
        rows = []
        for row in self.rows_listed(grid):
            rows.append(self.int_list(row))
        return rows

