class PlaintextHandler:

    @staticmethod
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
    def mutate(plain_input):
        """
        Returns list of possible inputs.
        """
        fuzzed = []
        bad_strings = PlaintextHandler.bad_strings()

        fuzzed = fuzzed + bad_strings

        # change individual lines
        lines = plain_input.splitlines()
        if len(lines) > 1:
            for i in range(len(lines)):
                for string in bad_strings:
                    lines_copy = lines.copy()
                    lines_copy[i] = string
                    fuzzed.append('\n'.join(lines_copy))

        return [PlaintextHandler.string_to_byte(f) for f in fuzzed]

    @staticmethod
    def parse_input(plain_input):
        """
        Returns inputs to the harness.
        """
        return PlaintextHandler.mutate(plain_input)
    
    @staticmethod
    def send_plaintext():
        return "plaintext"