import os
import json
from services.Harness import Harness

def main():
    harness = Harness()

    example_folder = './example_inputs'
    binary_folder = './binaries'
    for filename in os.listdir(example_folder):
        print('Opened: ', filename)
        if not harness.check_binary_exists(filename):
            continue

        example_path = os.path.join(example_folder, filename)
        binary_path = os.path.join(binary_folder, os.path.splitext(os.path.basename(filename))[0])
        inputs = harness.get_input(example_path)

        if inputs is False:
            return
        
        # If the input produces an error, write the input as a new line to output file
        for i in inputs:

            # If payload is a dictionary, convert to JSON first
            if isinstance(i, dict):
                i = json.dumps(i)

            success, stdout, stderr, exit_code, crash_type = harness.run_binary(binary_path, i)
            if not success:
                harness.write_hax(i, filename, stdout, stderr, exit_code, crash_type)


if __name__ == '__main__':
    main()
