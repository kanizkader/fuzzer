import json
import random
import string
import subprocess

BINARY_FILE = './binaries/binaries/json1'
INPUT_FILE = './binaries/example_inputs/json1.txt'

def rand_str(length):
    # Can custom more: https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
    return ''.join(random.choices(string.ascii_letters, k=length)) 

def json_inputs(file):
    with open(file, 'w') as f:
        tmp_dict = {}
        tmp_dict['len'] = random.randint(1, 50)
        tmp_dict['input'] = rand_str(tmp_dict['len'])
        tmp_dict['more_data'] = ["a", "bb"]

        json.dump(tmp_dict, f)
       
def fuzz():
    for i in range(1,10):    
        file_name = f"./json_inputs/json1_{i}.txt"
        json_inputs(file_name)
        try:
            print("Filename - " + file_name + ":")
            
            # Run binary with input files
            with open(file_name, 'r') as input_file:
                result = subprocess.run(BINARY_FILE, stdin=input_file, capture_output=True, text=True, timeout=2)
            
            # Print stdout and stderr
            print("Stdout:")
            print(result.stdout)
            print("Stderr:")
            print(result.stderr)
            
        except Exception as e:
            print(f"Error occurred: {e}")
    
if __name__ == "__main__":    
    fuzz()
    