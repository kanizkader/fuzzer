import pathlib
import json
import csv
import mimetypes
from input_handlers import CSVHandler, JSONHandler, PDFHandler, PlaintextHandler, XMLHandler
import services.MutationHelper as mh

class InputResolver:
    """
    Given example input, determines the relevant file type handler 
    based on the content of the .txt file and returns the output
    from respective handler.
    """

    @staticmethod
    def getInput(example_input_path):
        # Assume example_input is a file path
        file_path = pathlib.Path(example_input_path)

        with open(file_path, 'r') as file:
            content = file.read()

        data_type = InputResolver._detect_data_type(content)
        
        # Bit flips & byte flips
        general_mutations = [flip for flip in mh.flip(content.encode(), 200)]
        # Various empty strings
        general_mutations += [b'\x00', b'\n', b'', b'\r', b'\r\n']
        
        # Return fuzzed inputs, both format specific and general mutations
        if data_type == "csv":
            format_specific = CSVHandler.CsvHandler.parse_input(content)  
        elif data_type == "json":
            format_specific = JSONHandler.JSONHandler.parse_input(content)
        elif data_type == "pdf":
            format_specific = PDFHandler.PdfHandler.parse_input(content)
        elif data_type == None and mimetypes.guess_type(file_path)[0] == 'text/plain':
            format_specific = PlaintextHandler.PlaintextHandler.parse_input(content)
        else:
            print("I have no idea what file type this is lol")
            format_specific = []

        return format_specific + general_mutations

    @staticmethod
    def _detect_data_type(content):
        try:
            json.loads(content)
            return "json"
        except json.JSONDecodeError:
            pass

        try:
            csv.Sniffer().sniff(content)
            return "csv"
        except csv.Error:
            pass

        # Check for PDF (not yet ready for the real world)
        if content.startswith('%PDF-'):
            return "pdf"

        # If none of the above, return unknown
        return None
