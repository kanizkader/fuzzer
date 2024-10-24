import csv
import random
import string

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

        random.seed(123)
        while True:
            i = random.randrange(0, 3)
            if i == 2:
                yield next(bad)
            else:
                yield next(valid)
    
    @staticmethod
    def byte_flip():
        """
        Flips random bytes for each value in given JSON input
        Returns result as strings in JSON
        """
        random.seed(123)
        
        while True:
            length = random.randrange(20) # Can change max input length
            randStr = ''.join(random.choice(string.printable) for _ in range(length))
            randStr = randStr.replace(',', '') # remove commas
            print(randStr)
            yield randStr

    @staticmethod
    def mutate(inputs, schema, max_variants):
        """
        Expands a given list of inputs with mutations.
        """
        field = __class__.yield_input(schema)
        flip = __class__.byte_flip()

        for _ in range(max_variants):
            i = schema.header + '\n'.join(','.join(next(field) for _ in range(schema.num_cols)) 
                                          for _ in range(schema.num_rows))
            inputs.append(i)

        #for _ in range(max_variants):
            #i = schema.header + '\n'.join(','.join(next(flip) for _ in range(schema.num_cols)) 
                                          #for _ in range(schema.num_rows))
            #print(f'{i}\n')
            #inputs.append(i)


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

        for num in (16, 64, 256, 1024):
            # Add many rows
            inputs.append(schema.header +
                          __class__.format_row('abcdefgh', schema.num_cols) * num)

            # Many columns
            inputs.append(schema.header +
                          __class__.format_row('abcdefgh', num) * schema.num_rows)

            # Long cell contents
            inputs.append(schema.header +
                          __class__.format_row('abc' * num, schema.num_cols) * schema.num_rows)
      
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
                    s.header = rows[i] + '\n'
                    s.num_rows -= 1
                    continue
            for cell in cells:
                s.valid_inputs.add(cell)

        return __class__.fuzz(s)

    @staticmethod
    def send_csv():
        return "csv"
