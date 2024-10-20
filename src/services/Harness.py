import subprocess
import os
import logging
import pathlib
from .InputResolver import InputResolver

class Harness:
    """
    Harness your power and do stuff if you really want to.
    This class is entirely optional, including the entire services module.
    It is only there if we end up needing to do something more complex than
    just executing and calling everything from the fuzzer.py file. It might help
    clean things up a bit later down the line.
    """

    def __init__(self):
        pass

    @staticmethod
    def send_hArNesS():
        return "hArNesS"

    @staticmethod
    def check_binary_exists(example):
        """
        Given the file name of the example input, checks if there is a corresponding binary file.
        """
        binaries_folder = 'binaries'
        filename = os.path.splitext(os.path.basename(example))[0]
        binary = os.path.join(binaries_folder, filename)
        print(f'Checking that {binary} exists')
        return os.path.exists(binary)

    @staticmethod
    def get_input(example_input):
        """
        Collects a list of bad input based on the given example input
        """
        try:
            return InputResolver.getInput(example_input)
        except Exception as e:
            logging.error(f"An error occurred while collecting input: {e}")

    @staticmethod
    def run_binary(binary_path, payload):
        """
        Run a binary executable and capture all output (stdout, stderr).
        Provides detailed error information if something goes wrong.
        """        
        try:
            process = subprocess.run(
                [binary_path], 
                input=payload,
                capture_output=True, 
                text=True, 
                check=True,
                shell=True
            )
            # Print the program output
            print(f"Running '{binary_path}' with input '{payload}'\n")
            print(f"Standard Output:\n{process.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running '{binary_path}' with input '{payload}': {e}")
            print(f"Exit Code: {e.returncode}")
            print(f"Standard Output:\n{e.stdout}")
            print(f"Standard Error:\n{e.stderr}")
            return False
        except FileNotFoundError as fnf_error:
            print(f"File not found: {binary_path}. Error: {fnf_error}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
        return True

    @staticmethod
    def write_hax(bad_input, filename):
        """
        Writes output to a file and logs errors if anything goes wrong.
        """

        # Create output file
        output_folder = 'fuzzer_output'
        if not os.path.exists(output_folder):
            print(f"Folder '{output_folder}' does not exist.")
            return
        output_file = os.path.join(output_folder, 'bad_' + os.path.splitext(os.path.basename(filename))[0] + '.txt')
        
        try:
            with open(output_file, 'a') as f:
                print(f"Writing bad input to '{output_file}' via Harness\n")
                f.write(bad_input)
                f.write('\n')
        except Exception as e:
            logging.error(f"An error occurred while writing to the file: {e}")
            print(f"An error occurred while writing to the file: {e}")