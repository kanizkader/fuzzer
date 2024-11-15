from pwn import *
from .PDFHelper import PDFHelper 

class PdfHandler:
    @staticmethod
    def bad_strings():
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            content = bad_strings.read()
            bad_string_options = content.split("\n")                   
        return bad_string_options

    @staticmethod
    def string_to_byte(string):
        return string.encode()

    @staticmethod
    def mutate(plain_input):
        """
        Apply fuzzing to plain text input.
        """
        fuzzing_options = [
            PDFHelper.simple_buffer_overflow  
        ]
        
        # Append original input
        fuzzed = []
        fuzzed.append(plain_input) 

        try:
            if plain_input[-1] == "\n":
                plain_input = plain_input[:-1]
        except:
            pass
        
        # Apply individual fuzzing options
        for fuzz in fuzzing_options:
            fuzzed.append(fuzz(plain_input))
        
        # Apply bad strings 
        bad_strings = PDFHelper.get_bad_strings()
        for string in bad_strings:
            fuzzed.append(PDFHelper.put_bad_string(plain_input, string))
            
        # Apply format string options
        fmts = PDFHelper.get_format_str()
        for fmt in fmts:
            fuzzed.append(PDFHelper.put_format_str(plain_input, fmt))
            
        # Apply byte flips
        # for i in range(40):
        #     fuzzed.append(PDFHelper.byte_flip_string(plain_input)) 
        
        # Buffer Overflow 
        for bo in range(0, 8000, 1000):
            fuzzed.append(f"{cyclic(bo)}")
        
        return fuzzed
    
    @staticmethod
    def parse_input(content):
        """
        Parses pdf and returns a list of possible input strings for harness.
        """
        pattern = r"\((.*?)\) Tj"
        matched = re.findall(pattern, content)
        matched = matched[0]
        
        mutated_matches = PdfHandler.mutate(matched)
        modified_content = []
        for match in mutated_matches:
            content_copy = content
            modified_content.append(content_copy.replace(matched, match).encode())

        return modified_content