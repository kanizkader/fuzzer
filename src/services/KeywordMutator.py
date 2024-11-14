import subprocess


class KeywordMutator:
    """
    A class that first disassembles the C binary, identifies keywords of note,
    and thenmutates the input based on the keywords.
    """

    def __init__(self):
        pass

    @staticmethod
    def extract_strings(binary_path):
        """
        Extracts strings from the binary using strings command
        """
        result = subprocess.run(
            ["strings", binary_path], capture_output=True, text=True
        )
        strings = result.stdout.splitlines()
        filtered_strings = KeywordMutator.__filter_junk(strings)
        
        return filtered_strings

    @staticmethod
    def filter_vulnerable_functions(strings):
        """
        Filters out vulnerable stdlib functions from the binary.
        """
        vulnerable_functions = [
            "strcpy",
            "strcat",
            "sprintf",
            "scanf",
            "fgets",
            "gets",
            "printf",
            "fprintf",
            "sprintf",
            "snprintf",
            "vsprintf",
            "vsnprintf",
        ]
        return [
            s
            for s in strings
            if any(func in s for func in vulnerable_functions)
        ]

    @staticmethod
    def filter_files(strings):
        """
        Filters out file names from the strings. Not callable.
        """
        return [s for s in strings if ".c" in s or ".h" in s or ".o" in s]

    def __filter_junk(strings):
        """
        Filters out keywords that are not part of the standard library.
        """
        # Filter out junk
        filtered_strings = [s for s in strings if len(s) > 3]
        # Filter out std_lib calls
        filtered_strings = [s for s in filtered_strings if not s.startswith("__")]
        # Filter out code sections
        filtered_strings = [s for s in filtered_strings if not s.startswith(".")]

        return filtered_strings


if __name__ == "__main__":
    strings = KeywordMutator.extract_strings("binaries/binaries/csv1")
    for string in strings:
        print(string)

    vulnerable_functions = KeywordMutator.filter_vulnerable_functions(strings)
    files = KeywordMutator.filter_files(strings)
    print("\nVulnerable functions:")
    for func in vulnerable_functions:
        print(func)
    print("\nFiles:")
    for file in files:
        print(file)
