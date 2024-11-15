import logging
import os

empty_line = "|".ljust(38, " ") * 2 + "|\n"
bottom_line = "|".ljust(38, "_") * 2 + "|\n"

keys = {134: "Buffer overflow", 126: "Permission denied", 127: "Command not found", 128: "Fatal error",
        130: "Keyboard interrupt", 139: "Segfault", 143: "Terminated", "hang": "Hang (timeout)"}

class SummaryPrinter:
    """
    Prints results of fuzz testing to file.
    """
    def __init__(self, num_inputs, hax, filename, exec_time):
        self.num_inputs = num_inputs
        self.hax = hax
        self.filename = filename
        self.exec_time = exec_time
        self.crash_types = {}

        for hack in self.hax:
            if self.crash_types.get(keys[hack.exit_code]):
                self.crash_types[keys[hack.exit_code]] += 1
            else:
                self.crash_types[keys[hack.exit_code]] = 1
    
    def write_to_file(self):
        # Create output file
        output_folder = 'fuzzer_output'
        if not os.path.exists(output_folder):
            print(f"Folder '{output_folder}' does not exist.")
            return
        output_file = os.path.join(output_folder, 'bad_' + os.path.splitext(os.path.basename(self.filename))[0] + '.txt')

        time_per_input = (self.exec_time / self.num_inputs) * 1000

        try:
            with open(output_file, 'w') as f:
                f.write(f"Results summary: {self.filename}\n")
                f.write("\n")
                f.write("___ Timing ".ljust(38, "_") + " ___ Inputs & crashes ".ljust(38, "_") + "\n")
                f.write(empty_line)
                f.write(f"| Total runtime: {self.exec_time:.2f} secs".ljust(38, " ") + f"| Total inputs tried: {self.num_inputs}".ljust(38, " ") + "|\n")
                f.write(f"| Avg, runtime per input: {time_per_input:.2f} msec".ljust(38, " ") + f"| Number of crashes detected: {len(self.hax)}".ljust(38, " ") + "|\n")
                f.write(bottom_line + empty_line)
                f.write("| Crash types detected:".ljust(38, " ") + "|".ljust(38, " ") + "|\n")
                for key in self.crash_types:
                    f.write(f"| [{self.crash_types[key]:3d}] {key}".ljust(38, " ") + "|".ljust(38, " ") + "|\n")
                f.write(bottom_line)
                f.write("\n")
                f.write("Found the following inputs which trigger a crash:\n")
                f.write("\n")

                for hack in self.hax:
                    f.write("----------------------------------------------------------------\n")
                    f.write(f"Input:\n{hack.input}\n\n")
                    if hack.stdout:
                        f.write(f"Standard Output:\n{hack.stdout}\n")
                    if hack.stderr:
                        f.write(f"Standard Error:\n{hack.stderr}\n")
                    if hack.exit_code is not None:
                        f.write(f"Exit Code:\n{hack.exit_code}\n\n")
                    if hack.crash_type is not None:
                        f.write(f"Possible Crash Type:\n{hack.crash_type}\n")
                    f.write('\n')
        except Exception as e:
            logging.error(f"An error occurred while writing to the file: {e}")
            print(f"An error occurred while writing to the file: {e}")
