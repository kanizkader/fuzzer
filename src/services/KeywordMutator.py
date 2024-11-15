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
    def filter_vulnerable_keywords(strings):
        """
        Filters strings that contain common keywords from a predefined list.
        """
        try:
            keywords_path = "src/input_handlers/common-keywords.txt"
            with open(keywords_path, "r") as f:
                keywords = [line.strip() for line in f.readlines() if line.strip()]
                
            filtered = []
            for s in strings:
                for keyword in keywords:
                    if keyword.lower() in s.lower():
                        filtered.append(s)
                        break
            
            return filtered
            
        except FileNotFoundError:
            return []
        except Exception:
            return []

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

    @staticmethod
    def analyze_binary(binary_path):
        """
        Analyzes a binary file to extract strings, vulnerable keywords and files.
        Returns a tuple of (strings, vulnerable_keywords, files).
        """
        strings = KeywordMutator.extract_strings(binary_path)
        vulnerable_keywords = KeywordMutator.filter_vulnerable_keywords(strings)
        files = KeywordMutator.filter_files(strings)
        
        print("\nInteresting keywords:")
        for keyword in vulnerable_keywords:
            print(keyword)
        print("\nFiles detected:")
        for file in files:
            print(file)
            
        return strings, vulnerable_keywords, files


if __name__ == "__main__":
    KeywordMutator.analyze_binary("binaries/csv1")
