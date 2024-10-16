import subprocess
import os
import logging
from input_handlers import json_handler, pdf_handler

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
    def run_binary(binary_path):
        """
        Run a binary executable and capture all output (stdout, stderr).
        Provides detailed error information if something goes wrong.
        """
        try:
            process = subprocess.run(
                [binary_path], 
                capture_output=True, 
                text=True, 
                check=True,
                shell=True
            )
            # Print the program output
            print("Running binary via Harness")
            print(f"Standard Output:\n{process.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the binary: {e}")
            print(f"Exit Code: {e.returncode}")
            print(f"Standard Output:\n{e.stdout}")
            print(f"Standard Error:\n{e.stderr}")
        except FileNotFoundError as fnf_error:
            print(f"File not found: {binary_path}. Error: {fnf_error}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    @staticmethod
    def write_hax():
        """
        Writes output to a file and logs errors if anything goes wrong.
        """
        output_folder = 'fuzzer_output'
        if not os.path.exists(output_folder):
            print(f"Folder '{output_folder}' does not exist.")
            return

        output_file = os.path.join(output_folder, 'test_output2.txt')
        try:
            with open(output_file, 'w') as f:
                print("Writing fuzzer output via Harness")
                f.write('Test output\n')
                f.write(json_handler.JsonHandler.send_json() + '\n')
                f.write(pdf_handler.PdfHandler.send_pdf() + '\n')
        except Exception as e:
            logging.error(f"An error occurred while writing to the file: {e}")
            print(f"An error occurred while writing to the file: {e}")