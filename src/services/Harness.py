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
        
        Returns True/False, stdout, stderr, returncode
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
            return True, process.stdout, process.stderr, process.returncode, None
        except subprocess.CalledProcessError as e:
            crash_type = Harness.detect_crash(e.returncode)
            print(f"An error occurred while running '{binary_path}' with input '{payload}': {e}")
            print(f"Exit Code: {e.returncode}")
            print(f"Standard Output:\n{e.stdout}")
            print(f"Standard Error:\n{e.stderr}")
            print(f"Possible Crash Type: \n{crash_type}")
            return False, e.stdout, e.stderr, e.returncode, crash_type
        except FileNotFoundError as fnf_error:
            print(f"File not found: {binary_path}. Error: {fnf_error}")
            return False, None, str(fnf_error), None, None
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
            return False, None, str(ex), None, None
        # return True

    @staticmethod
    def write_hax(bad_input, filename, stdout=None, stderr=None, exit_code=None, crash_type=None):
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
                if exit_code != 134:
                    print(f"Writing bad input to '{output_file}' via Harness\n")
                    f.write("----------------------------------------------------------------\n")
                    f.write(f"Input:\n{bad_input}\n\n")
                    if stdout:
                        f.write(f"Standard Output:\n{stdout}\n")
                    if stderr:
                        f.write(f"Standard Error:\n{stderr}\n")
                    if exit_code is not None:
                        f.write(f"Exit Code:\n{exit_code}\n\n")
                    if crash_type is not None:
                        f.write(f"Possible Crash Type:\n{crash_type}\n")
                    f.write('\n')
        except Exception as e:
            logging.error(f"An error occurred while writing to the file: {e}")
            print(f"An error occurred while writing to the file: {e}")
            
    @staticmethod
    def detect_crash(exit_code):
        """
        Looks at exit code and identifies possible type of crash.
        """
        if exit_code == 2:
            return "Incorrect command (or argument) usage."
        elif exit_code == 126:
            return "Permission denied (or) unable to execute."
        elif exit_code == 127:
            return "Command not found, or PATH error."
        elif exit_code == 128:
            return "Command terminated externally by passing signals, or it encountered a fatal error."
        elif exit_code == 130:
            return "Termination by Ctrl+C or SIGINT (termination code 2 or keyboard interrupt)."
        elif exit_code == 134:
             return "Termination by SIGABRT (signal aborted) -- IGNORED."
        elif exit_code == 139:
            return "Termination by SIGSEV (segmentation fault)."
        elif exit_code == 143:
            return "Termination by SIGTERM (default termination)."
        
        return None
