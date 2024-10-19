import csv

class Schema:
    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.has_header = False
        self.header = []
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
        or empty string if row is empty
        """
        if len(row) == 0:
            return ''
        else:
            return ','.join(cell for cell in row) + '\n'

    @staticmethod
    def format_table(table):
        """
        Returns table in csv format
        """
        return ''.join(__class__.format_row(row) for row in table)

    @staticmethod
    def bad_row(schema):
        """
        Returns mutated row of given file based on known
        bad inputs. Filepath will need to be changed.
        """
        i = 0

        with open('/src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')): 
                    bad_row = [cell for cell in schema.first_row]
                    bad_row[i % schema.num_cols] = bad_string[:-1]
                    i += 1
                    yield bad_row

    @staticmethod
    def mutate(inputs, schema, max_variants):
        """
        Expands a given list of inputs with up to max_variants mutations.
        """
        bad_row = __class__.bad_row(schema)

        for _ in range(max_variants):
            var = [schema.header]
            for _ in range(schema.num_rows):
                var.append(next(bad_row))
            v1 = __class__.format_table(var)
            print(v1, '\n')
            inputs.append(v1)
        return inputs

    @staticmethod
    def fuzz(schema):
        """
        Makes list of fuzzer inputs
        """
        # Start with empty string
        inputs = ['']
        # Add empty table
        empty = __class__.format_row(['' for _ in range(schema.num_cols)])
        inputs.append(__class__.format_row(schema.header) + empty)

        # Add many rows
        inputs.append(__class__.format_row(schema.header) +
                      __class__.format_row(['A' for _ in range(schema.num_cols)]) * 1000)
        # Many more rows
        inputs.append(__class__.format_row(schema.header) +
                      __class__.format_row(['A' for _ in range(schema.num_cols)]) * 100000)

        return __class__.mutate(inputs, schema, 100)

    @staticmethod 
    def parse_input(filepath):
        """
        Opens csv file, parses format and constructs mutations.
        Currently returns a list but could be modified depending
        on what format the harness expects.
        """
        s = Schema()

        with open(filepath, 'r') as csvfile:
            if csv.Sniffer().has_header(csvfile.read(1024)):
               s.has_header = True
            csvfile.seek(0)
            reader = csv.reader(csvfile, delimiter=',')
            num_rows = 0

            if s.has_header:
                s.header = __class__.split_cells(next(reader))
            for row in reader:
                if num_rows == 0:
                    s.first_row = __class__.split_cells(row)
                    s.num_cols = len(s.first_row)
                num_rows += 1
            s.num_rows = num_rows

        return __class__.fuzz(s)

    @staticmethod
    def send_csv():
        return "csv"
