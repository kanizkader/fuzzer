from pwn import *
import json
from .PlaintextHelper import PlaintextHelper 

class PlaintextHandler:
    @staticmethod
    def bad_strings():
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            content = bad_strings.read()
            bad_string_options = content.split("\n")                   
        return bad_string_options

    @staticmethod
    def string_to_byte(string):
        return string.encode()

    @staticmethod
    def mutate(plain_input):
        """
        Apply fuzzing to plain text input.
        """
        fuzzing_options = [
            PlaintextHelper.simple_buffer_overflow  
        ]
        
        # Append original input
        fuzzed = []
        fuzzed.append(plain_input) 

        try:
            if plain_input[-1] == "\n":
                plain_input = plain_input[:-1]
        except:
            pass
        
        # Apply individual fuzzing options
        for fuzz in fuzzing_options:
            fuzzed.append(fuzz(plain_input))
        
        # Apply bad strings 
        bad_strings = PlaintextHelper.get_bad_strings()
        for string in bad_strings:
            fuzzed.append(PlaintextHelper.put_bad_string(plain_input, string))
            
        # Apply format string options
        fmts = PlaintextHelper.get_format_str()
        for fmt in fmts:
            fuzzed.append(PlaintextHelper.put_format_str(plain_input, fmt))
            
        # Apply byte flips
        # for i in range(40):
        #     fuzzed.append(PlaintextHelper.byte_flip_string(plain_input)) 
        
        # Buffer Overflow 
        for bo in range(0, 8000, 1000):
            fuzzed.append(f"{cyclic(bo)}")
        
        fuzzed_bytes = [PlaintextHandler.string_to_byte(item) for item in fuzzed]
        return fuzzed_bytes

    @staticmethod
    def parse_input(content):
        """
        Parses plain text and returns a list of possible input strings for harness.
        """
        return PlaintextHandler.mutate(content)
