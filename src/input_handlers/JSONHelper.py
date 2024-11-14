import random
import json

class JSONHelper:
    @staticmethod
    def simple_buffer_overflow(json_input):
        return {key: f"{value * 1000}" for key, value in json_input.items()}
    
    @staticmethod
    def bigger_buffer_overflow(json_input):
        return {key: f"{value * 8000}" for key, value in json_input.items()}
    
    @staticmethod
    def malformed_json(json_input):
        malformed = json.dumps(json_input)
        return malformed.replace("}", "")
    
    @staticmethod
    def biggest_int(json_input):
        results = {}
        for key, value in json_input.items():
            if isinstance(value, int):
                results[key] = 2147483647
        return results
    
    @staticmethod
    def int_overflow(json_input):
        results = {}
        for key, value in json_input.items():
            if isinstance(value, int):
                results[key] = value + 2147483647
        return results
    
    @staticmethod
    def int_underflow(json_input):
        results = {}
        for key, value in json_input.items():
            if isinstance(value, int):
                results[key] = value - 2147483647
        return results
    
    @staticmethod
    def long_keys(json_input):
        results = {}
        for key, value in json_input.items():
            long_key = key + 'A' * 1000
            results[long_key] = value
        return results
    
    @staticmethod
    def invalid_types(json_input):
        results = {}
        for key, value in json_input.items():
            if isinstance(value, int):
                results[key] = str(value)   # Change integers to strings
            elif isinstance(value, str):
                results[key] = int(value)         # Change strings to integers
            elif isinstance(value, bool):
                results[key] = 0            # Change booleans to integers
            else:
                results[key] = value
        return results
    
    @staticmethod
    def get_bad_strings():
        """
        Returns bad strings as a list
        """
        bad_string_options = []
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')):
                    bad_string_options.append(bad_string.strip('\n'))
            
        return bad_string_options
    
    @staticmethod
    def put_bad_string(json_input, string):
        """
        Appends bad string to the end of the input in dictionary.
        """
        results = {}
        for key, value in json_input.items():
            if isinstance(value, list):
                vals = []
                for item in value:
                    vals.append(f"{item}{string}")
                results[key] = vals
            else:
                results[key] = f"{value}{string}"
            
        return results
    
    @staticmethod
    def get_format_str():
        """
        Returns list of format string options
        """
        return ['%s', '%d', '%x', '%p', '%n']
    
    @staticmethod
    def put_format_str(json_input, format_string):
        """
        Injects diff format string options
        """
        return {key: f"{value}{format_string * 1000}" for key, value in json_input.items()}

    @staticmethod
    def byte_flip_string(json_input):
        """
        Flips random bytes for each value in given JSON input
        Returns result as strings in JSON
        """
        random.seed()
        new_input = json_input.copy()

        for key, value in new_input.items():
            bytearr = bytearray(str(value).encode('utf-8'))

            for i in range(20): # Can change the number of flipped bytes
                byte = random.randrange(128) # 128 byte ASCII value
                pos = random.randrange(len(bytearr))
                bytearr[pos] = byte ^ 1
            
            new_input[key] = bytearr.decode('utf-8')
        
        return new_input