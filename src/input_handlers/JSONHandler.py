import json
# import subprocess # for local testing
# import os # for local testing
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

################################################################
# Local Testing - REMOVE LATER 
################################################################
"""
if __name__ == "__main__":
    filepath = "./binaries/example_inputs/json1.txt"
    inputs = JSONHandler.parse_input(filepath)

    # Print fuzzed inputs
    j = 0
    for i in inputs:
        print(f"---- Fuzz {j} -----")
        # print(i)
        file_name = f'{j}.txt'
        try:
            print("Filename - " + file_name + ":")
            
            with open(file_name, 'w') as f:
                json.dump(i, f)
            
            # Run binary with input files
            with open(file_name, 'r') as input_file:
                result = subprocess.run('./binaries/binaries/json1', stdin=input_file, capture_output=True, text=True, timeout=2)
            
            # Print stdout and stderr
            print("Stdout:")
            print(result.stdout)
            print("Stderr:")
            print(result.stderr)
            
        except Exception as e:
            print(f"Error occurred: {e}")
            
        os.remove(file_name)
            
        j += 1
"""        
