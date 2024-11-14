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
    def xml_strings():
        bad_string_options = []
        with open('./src/input_handlers/xml-strings.txt', 'r') as bad_strings:
            contents = bad_strings.read()
            contents = contents.replace('\n', ' ')
            for entry in contents.split(',,,'):
                bad_string_options.append(entry)
        return bad_string_options

    @staticmethod
    def sub_bad_strings(base_input, bad_strings, properties, content):
        """
        Replaces values in base input with bad strings
        """
        fuzzed = []

        for string in bad_strings:
            for p in properties:
                if any(c in string for c in ('"', '\\')):
                    continue
                subbed = re.sub(p, string, base_input)
                fuzzed.append(subbed)

            for c in content:
                if any(c in string for c in ('>', '<', '\\')):
                    continue
                subbed = re.sub(c, string, base_input)
                fuzzed.append(subbed)
            
            if any(c in bad_strings for c in ('>', '<')):
                continue
            subbed = f'<{string}></{string}>'
            fuzzed.append(subbed)
        
        return fuzzed
    
    @staticmethod
    def buffer_overflow(length):
        """
        Returns array of long strings of the given length
        """
        fuzzed = []
        # create nested divs
        nested = "<div>"
        for _ in range(length):
            nested = f"<div>{nested}</div>"
        nested += "</div>"
        fuzzed.append(nested)

        # Just opening tags
        fuzzed.append("<div>" * length)
        
        # Just letters
        fuzzed.append("a" * length)

        # Just numbers
        fuzzed.append("1" * length)

        return fuzzed

    @staticmethod
    def mutate(base_input):
        """
        Returns list of possible inputs.
        """
        fuzzed = []
        bad_strings = XMLHandler.bad_strings()
        length = 512

        # find all property strings 
        properties = re.findall('"([^"]*)"', base_input)
        # find all tagged strings
        content = re.findall(r'>(.+?)<', base_input)

        fuzzed += XMLHandler.sub_bad_strings(base_input, bad_strings, properties, content)
        fuzzed += XMLHandler.buffer_overflow(length)

        for bad in bad_strings:
            many_links = f"<a href='aaaa'>Link</a>" * length + f"<a href='aaaa'>{bad}</a>"
            fuzzed.append(many_links)

        # Classic XXE
        xml_strings = XMLHandler.xml_strings()
        for x in xml_strings:
            fuzzed.append(x)

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