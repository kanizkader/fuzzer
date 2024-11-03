import re

class XMLHandler:
    def string_to_byte(string):
        return string.encode()

    @staticmethod
    def bad_strings():
        bad_string_options = []
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')):
                    bad_string_options.append(bad_string.strip('\n'))
        return bad_string_options

    @staticmethod
    def mutate(base_input):
        """
        Returns list of possible inputs.
        """
        fuzzed = []
        bad_strings = XMLHandler.bad_strings()

        # find all property strings 
        properties = re.findall('"([^"]*)"', base_input)
        # find all tagged strings
        strings = re.findall(r'>(.+?)<', base_input)

        for p in properties:
            for string in bad_strings:
                if any(c in string for c in ('"', '\\')):
                    continue
                subbed = re.sub(p, string, base_input)
                fuzzed.append(subbed)
        
        for s in strings:
            for string in bad_strings:
                if any(c in string for c in ('>', '<', '\\')):
                    continue
                subbed = re.sub(s, string, base_input)
                fuzzed.append(subbed)
                
        return [XMLHandler.string_to_byte(f) for f in fuzzed]

    @staticmethod
    def parse_input(base_input):
        """
        Returns inputs to the harness.
        """
        return XMLHandler.mutate(base_input)
    
    @staticmethod
    def send_xml():
        return "xml"