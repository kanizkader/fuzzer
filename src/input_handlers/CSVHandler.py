import csv

class Schema:
    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.has_header = False
        self.header = ''
        self.valid_inputs = set()

class CsvHandler:
    @staticmethod
    def format_row(char, num_cols):
        """
        Returns a formatted csv row containing num_cols * char
        """
        return ','.join(char for _ in range(num_cols)) + '\n'
        
    @staticmethod
    def yield_valid(schema):
        """
        Yields a single valid cell/field
        """
        inputs = list(schema.valid_inputs)

        i = 0
        while True:
            yield inputs[i]
            i = (i + 1) % len(inputs)

    @staticmethod
    def yield_bad():
        """
        Yields a single fuzzed cell/field.
        Note path to input file may need to be changed.
        """
        store = []
        with open('/src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')):
                    store.append(bad_string[:-1])

        i = 0
        while True:
            yield store[i]
            i = (i + 1) % len(store)
    
    @staticmethod
    def yield_input(schema):
        """
        Yields a single cell/field, alternating
        between valid and fuzzed inputs
        """
        valid = __class__.yield_valid(schema)
        bad = __class__.yield_bad()

        i = 0
        while True:
            if i % 2 == 0:
                yield next(valid)
            else:
                yield next(bad)
            i += 1

    @staticmethod
    def mutate(inputs, schema, max_variants):
        """
        Expands a given list of inputs with mutations.
        """
        field = __class__.yield_input(schema)

        for _ in range(max_variants):
            i = schema.header + '\n'.join(','.join(next(field) for _ in range(schema.num_cols)) 
                                          for _ in range(schema.num_rows))
            inputs.append(i)

        return inputs

    @staticmethod
    def fuzz(schema):
        """
        Makes list of fuzzer inputs
        Starting with various empty strings
        """
        inputs = ['\0', '\n', '', '\r']
        # Add empty table
        inputs.append(schema.header + __class__.format_row('', schema.num_cols))

        for num in (64, 256, 1024, 4096):
            # Add many rows
            inputs.append(schema.header +
                          __class__.format_row('A', schema.num_cols) * num)

            # Many columns
            inputs.append(schema.header +
                          __class__.format_row('A', num) * schema.num_rows)
      
        # Then mutate based on detected schema
        return __class__.mutate(inputs, schema, 200)

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
                s.header = ','.join(cell for cell in next(reader)) + '\n'
            for row in reader:
                if num_rows == 0:
                    s.num_cols = len(row)
                for cell in row:
                    s.valid_inputs.add(cell)
                num_rows += 1
            s.num_rows = num_rows

        return __class__.fuzz(s)

    @staticmethod
    def send_csv():
        return "csv"