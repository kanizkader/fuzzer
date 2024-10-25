import json
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
        
        # Apply individual fuzzing options
        fuzzed = []
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

        # Apply byte flips
        for i in range(40):
            fuzzed.append(JSONHelper.byte_flip_string(json_input)) 

        # Apply byte flips
        #for i in range(40):
        #    fuzzed.append(JSONHelper.byte_flip(json_input)) 
            
        return fuzzed

    @staticmethod
    def parse_input(content):
        """
        Parses JSON and returns list of possible input dictionaries for harness.
        """
        data = json.loads(content)
        if isinstance(data, list):
            fuzzed = []
            for item in data:
                fuzzed.extend(JSONHandler.mutate(item))
            return fuzzed_inputs
        else:
            return JSONHandler.mutate(data)
    
    @staticmethod
    def send_json():
        return "json"
