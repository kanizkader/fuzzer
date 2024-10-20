class JSONHelper:
    @staticmethod
    def simple_buffer_overflow(json_input):
        """
        Can remove this function later when we have better functions
        """
        return {key: f"{value * 1000}" for key, value in json_input.items()}
    
    @staticmethod
    def get_bad_strings():
        """
        Returns bad strings as a list
        """
        bad_string_options = []
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')):
                    bad_string_options.append(bad_string.strip('\n'))
            
        return bad_string_options
    
    @staticmethod
    def bad_string(json_input, string):
        """
        Appends bad string to the end of the input in dictionary.
        """
        results = {}
        for key, value in json_input.items():
            if isinstance(value, list):
                vals = []
                for item in value:
                    vals.append(f"{item}{string}")
                results[key] = vals
            else:
                results[key] = f"{value}{string}"
            
            
        return results