import csv
import random
import string
import services.MutationHelper as mh

random.seed(123)

class Schema:
    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.has_header = False
        self.header = b''
        self.valid_inputs = set()

class CsvHandler:
    @staticmethod
    def format_row(char, num_cols):
        """
        Returns a formatted csv row containing num_cols * char
        """
        return b','.join(char for _ in range(num_cols)) + b'\n'
        
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
    def yield_input(schema):
        """
        Yields a single cell/field, alternating
        between valid and fuzzed inputs
        """
        valid = __class__.yield_valid(schema)
        bad = mh.yield_bad_string()

        while True:
            i = random.randrange(0, 6)
            if i == 4:
                yield next(bad)
            if i == 5:
                yield (next(valid) + next(bad))
            else:
                yield next(valid)

    @staticmethod
    def mutate(inputs, schema, max_variants):
        """
        Expands a given list of inputs with mutations.
        """
        field = __class__.yield_input(schema)

        for _ in range(max_variants):
            i = schema.header + b'\n'.join(b','.join(next(field) for _ in range(schema.num_cols)) 
                                          for _ in range(schema.num_rows))
            inputs.append(i)

        return inputs

    @staticmethod
    def fuzz(csvfile, schema):
        """
        Makes list of fuzzer inputs
        Starting with various empty strings
        """
        inputs = [b'\x00', b'\n', b'', b'\r', b'\r\n']
        # Add empty table
        inputs.append(schema.header + __class__.format_row(b'', schema.num_cols))

        for num in (16, 64, 256, 1024):
            # Add many rows
            inputs.append(schema.header +
                          __class__.format_row(b'abcdefgh', schema.num_cols) * num)

            # Many columns
            inputs.append(schema.header +
                          __class__.format_row(b'abcdefgh', num) * schema.num_rows)

            # Long cell contents
            inputs.append(schema.header +
                          __class__.format_row(b'abc' * num, schema.num_cols) * schema.num_rows)

        # Then mutate based on detected schema
        return __class__.mutate(inputs, schema, 200)

    @staticmethod 
    def parse_input(csvfile):
        """
        Parses csv file format and constructs mutations.
        Currently returns a list but could be modified depending
        on what format the harness expects.
        """
        s = Schema()

        if csv.Sniffer().has_header(csvfile):
            s.has_header = True

        rows = csvfile.split('\n')
        if len(rows[-1]) == 0:
            rows.pop()
        s.num_rows = len(rows)

        for i in range(s.num_rows):
            # May need to look at regex split to avoid escaped chars
            cells = rows[i].split(',')
            if i == 0:
                s.num_cols = len(cells)
                if s.has_header:
                    h = rows[i] + '\n'
                    s.header = h.encode()
                    s.num_rows -= 1
                    continue
            for cell in cells:
                s.valid_inputs.add(cell.encode())
        
        return __class__.fuzz(csvfile, s)

    @staticmethod
    def send_csv():
        return "csv"
