import csv

class Schema:
    def __init__(self):
        self.num_rows = 0
        self.num_columns = 0
        self.header = 0
        self.first_row = []
        self.sep = ','

class CsvHandler:
    @staticmethod
    def split_cells(row):
        """
        Splits rows of input file into cells
        """
        return [cell for cell in row]

    @staticmethod
    def format_row(row):
        """
        Returns single row in csv format
        """
        return ','.join(cell for cell in row) + '\n'

    @staticmethod
    def format_table(table):
        """
        Returns table in csv format
        """
        return ''.join(__class__.format_row(row) for row in table)

    @staticmethod
    def mutate(schema):


    @staticmethod
    def fuzz(schema, has_header):
        """
        Makes list of fuzzer inputs
        """
        # Start with valid input
        inputs = [__class__.format_table(schema)]

        # Add empty string
        inputs.append('')
        # Add empty table
        empty = __class__.format_row(['' for _ in range(len(schema))])
        if has_header:
            inputs.append(__class__.format_row(schema[0]) + empty)
        else:
            inputs.append(empty)

        # Add many rows
        inputs.append(__class__.format_row(schema[0]) +
                      __class__.format_row(['A' for _ in range(len(schema[0]))]) * 1000)
        # Many more rows
        inputs.append(__class__.format_row(schema[0]) +
                      __class__.format_row(['A' for _ in range(len(schema[0]))]) * 100000)

        return inputs

    @staticmethod 
    def parse_input(filepath):
        """
        Opens csv file, parses format and constructs mutations.
        Currently returns a list but could be modified depending
        on what format the harness expects.
        """
        has_header = False
        schema = []

        with open(filepath, 'r') as csvfile:
            if csv.Sniffer().has_header(csvfile.read(1024)):
                has_header = True

        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            schema = [__class__.split_cells(row) for row in reader]

        return __class__.fuzz(schema, has_header)

    @staticmethod
    def send_csv():
        return "csv"