import subprocess
import os
import logging
import pathlib
from .InputResolver import InputResolver
from services.SummaryPrinter import SummaryPrinter

class Hack:
    def __init__(self, input_bytes, stdout, stderr, exit_code, crash_type):
        self.input = input_bytes
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.crash_type = crash_type

class Harness:
    """
    The harness runs each binary, communicates with the process, and records any 
    output and/or errors returned.
    """

    def __init__(self):
        pass

    @staticmethod
    def truncate(s, limit):
        if len(s) == 0:
            return ''
        if isinstance(s, bytearray):
            return s
        if len(s) > limit:
            return s[:limit] + b'...'
        else:
            return s

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
        success = False 
        crash_type = None

        try:
            process = subprocess.Popen(
                [binary_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            
            print(f'Running {binary_path}...'.ljust(32), f'Input: {__class__.truncate(payload, 26)}')
            stdout, stderr = process.communicate(payload, timeout=10)
            print(f'Return code: {process.returncode}'.ljust(32), f'Output: {__class__.truncate(stdout, 25)}')
            print(' ' * 32, f'Stderr: {__class__.truncate(stderr, 25)}\n')

            if process.returncode != 0:
                crash_type = Harness.detect_crash(process.returncode)
                print(f'[*] Possible crash detected: {crash_type}', end='')
                if process.returncode != 134 or b'stack smashing' in stderr:
                    print(f"[*] Action: Writing bad input to output file via Harness\n")
                else:
                    print(f'[*] Action: IGNORED\n')
            else:
                success = True
        except subprocess.TimeoutExpired:
            crash_type = Harness.detect_crash('hang')
            print(f'[*] Possible crash detected: {crash_type}', end='')
            print(f"[*] Action: Writing bad input to output file via Harness\n")
            process.kill()
            stdout, stderr = process.communicate()
            return success, stdout, stderr, 'HANG', crash_type
        except Exception as e:
            stdout = None
            stderr = None
            print(f'Error while running {binary_path}: {e}')
            return success, stdout, stderr, None, crash_type 

        return success, stdout, stderr, process.returncode, crash_type 

    @staticmethod
    def write_hax(num_inputs, hax, filename, execution_time):
        """
        Writes output to a file and logs errors if anything goes wrong.
        """
        sp = SummaryPrinter(num_inputs, hax, filename, execution_time)  
        sp.write_to_file() 
            
    @staticmethod
    def detect_crash(exit_code):
        """
        Looks at exit code and identifies possible type of crash.
        """
        if exit_code == 2:
            return "Incorrect command (or argument) usage.\n"
        elif exit_code == 126:
            return "Permission denied (or) unable to execute.\n"
        elif exit_code == 127:
            return "Command not found, or PATH error.\n"
        elif exit_code == 128:
            return "Command terminated externally by passing signals, or it encountered a fatal error.\n"
        elif exit_code == 130:
            return "Termination by Ctrl+C or SIGINT (termination code 2 or keyboard interrupt).\n"
        elif exit_code == 134:
            return "Termination by SIGABRT (signal aborted)\n"
        elif exit_code == 139:
            return "Termination by SIGSEV (segmentation fault).\n"
        elif exit_code == 143:
            return "Termination by SIGTERM (default termination).\n"
        elif exit_code == 'hang':
            return "Program hang (time out).\n"
        
        return None