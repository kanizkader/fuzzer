import random

class PlaintextHelper:

    @staticmethod
    def simple_buffer_overflow(plain_input):
        """
        Can remove this function later when we have better functions
        """
        return f"{plain_input * 1000}"

    @staticmethod
    def get_bad_strings():
        """
        Returns bad strings as a list.
        """
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            content = bad_strings.read()
            bad_string_options = content.split("\n")                   
        return bad_string_options
    
    @staticmethod
    def put_bad_string(plain_input, string):
        """
        Appends bad string to the end of the input.
        """
        return f"{plain_input}{string}"
    
    @staticmethod
    def get_format_str():
        """
        Returns list of format string options.
        """
        return ['%s', '%d', '%x', '%p', '%n']
    
    @staticmethod
    def put_format_str(plain_input, format_string):
        """
        Injects format string options into the input.
        """
        return f"{plain_input}{format_string * 200}"

    @staticmethod
    def byte_flip_string(plain_input):
        """
        Flips random bytes for the given plain input.
        Returns the result as a string.
        """
        random.seed()
        bytearr = bytearray(plain_input.encode('utf-8'))

        for i in range(20):  # Can change the number of flipped bytes
            byte = random.randrange(128)  # 128 byte ASCII value
            pos = random.randrange(len(bytearr))
            bytearr[pos] = byte ^ 1
        
        return bytearr.decode('utf-8')

    @staticmethod
    def byte_flip(plain_input):
        """
        Flips random bytes for the given plain input.
        Returns the result as raw bytes.
        """
        random.seed()
        bytearr = bytearray(plain_input.encode('utf-8'))

        for i in range(20):  # Can change the number of flipped bytes
            byte = random.randrange(256)
            pos = random.randrange(len(bytearr))
            bytearr[pos] = byte ^ 1
        
        return bytes(bytearr)
