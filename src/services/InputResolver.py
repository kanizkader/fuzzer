import pathlib
import json
import csv
import mimetypes
from input_handlers import CSVHandler, JSONHandler, PDFHandler, PlaintextHandler

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

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        data_type = InputResolver._detect_data_type(content)

        if data_type == "csv":
            return CSVHandler.CsvHandler.parse_input(content)
        elif data_type == "json":
            return JSONHandler.JSONHandler.parse_input(content)
        elif data_type == "pdf":
            return PDFHandler.PdfHandler.parse_input(content)
        #if mimetypes.guess_type(file_path)[0] == 'text/plain':
            #return PlaintextHandler.PlaintextHandler.parse_input(content)
        else:
            print("I have no idea what file type this is lol")
            return []

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
        return "idfk"
