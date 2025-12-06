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

    def process_data_as_rows(self, file_ix, strip_lines=True):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                if strip_lines:
                    data = file.read().strip()
                    return data.splitlines()
                else:
                    return [line.rstrip('\n') for line in file]
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def process_data_as_listed_rows(self, file_ix):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                data = file.read().strip()
            return [ list(row) for row in data.splitlines() ]
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def process_data_as_zip_rows(self, file_ix):
        """
        String rows are splitted in the first space.
        e.g. 'hello world' --> ['hello', 'world']
        """
        rows = self.process_data_as_rows(file_ix)
        if rows is None:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None
        else:
            return [ tuple(xs.split()) for xs in rows ]

    def process_data_as_zip_columns(self, file_ix):
        """
        Reads a file and returns a list of tuples where each tuple represents a column.
        Each line is split by whitespace, and the resulting values are zipped by column.
        e.g. '1 2 3\n4 5 6' --> [('1', '4'), ('2', '5'), ('3', '6')]
        """
        rows = self.process_data_as_rows(file_ix)
        if rows is None:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None
        else:
            # Split each row into columns and transpose rows to columns
            split_rows = [row.split() for row in rows]
            if not split_rows:
                return []
            # Transpose the matrix: rows become columns and vice versa
            return list(zip(*split_rows))

    def process_data_as_string(self, file_ix, eof_by="\n"):
        try:
            with open(self.file_paths[file_ix], 'r') as file:
                data = file.read().strip().replace("\n",eof_by)
            return data
        except FileNotFoundError:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None

    def process_data_as_blocks(self, file_ix):
        """
        Input of the form:

        AAA
        BBB

        CCC
        DDD

        Is transform in [[AAA, BBB], [CCC, DDD]]
        """
        string = self.process_data_as_string(file_ix)
        if string is None:
            print(f"Error: The file '{self.file_paths[file_ix]}' was not found.")
            return None
        else:
            return list(map(lambda xs : xs.splitlines(), string.split("\n\n")))

    def int_list(self, list_string):
        return [ int(x) for x in list_string ]

    def rows_listed(self, rows):
        return [ list(row) for row in rows ]

    def int_grid(self, grid):
        rows = []
        for row in self.rows_listed(grid):
            rows.append(self.int_list(row))
        return rows

