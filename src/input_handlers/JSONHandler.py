import json
from pwn import *
from .JSONHelper import JSONHelper

class JSONHandler:
    @staticmethod
    def mutate(json_input):
        """
        Apply fuzzing to python dictionary.
        """
        fuzzing_options = [
            JSONHelper.simple_buffer_overflow,
        ]
        
        # Append original input
        fuzzed = []
        fuzzed.append(json_input) 
        
        # Apply individual fuzzing options
        for fuzz in fuzzing_options:
            fuzzed.append(fuzz(json_input))
        
        # Apply bad strings 
        bad_strings = JSONHelper.get_bad_strings()
        for string in bad_strings:
            fuzzed.append(JSONHelper.put_bad_string(json_input, string))
            
        # Format String Options
        fmts = JSONHelper.get_format_str()
        for fmt in fmts:
            fuzzed.append(JSONHelper.put_format_str(json_input, fmt))
            
        # Buffer Overflow 
        for bo in range(0, 8000, 1000):
            fuzzed.append(f"{cyclic(bo)}")

        # Apply ASCII byte flips
        for i in range(40):
            fuzzed.append(JSONHelper.byte_flip_string(json_input)) 
            
        fuzzed_bytes = [json.dumps(item).encode() if isinstance(item, dict) else item.encode() for item in fuzzed]    
        return fuzzed_bytes

    @staticmethod
    def parse_input(content):
        """
        Parses JSON and returns list of possible input dictionaries for harness.
        """
        data = json.loads(content)

        fuzzed = []
        if isinstance(data, list):
            for item in data:
                fuzzed.extend(JSONHandler.mutate(item))
        else:
            fuzzed.extend(JSONHandler.mutate(data))
            
        return fuzzed
    
    @staticmethod
    def send_json():
        return "json"