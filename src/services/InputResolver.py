import pathlib
from input_handlers import CSVHandler, JSONHandler, PDFHandler

class InputResolver:
    """
    Given example input, calls the relevant file type handler 
    based on the filename and returns the output
    """

    @staticmethod
    def getInput(example_input):
        example_input = example_input.lower()

        match True:
            case _ if "csv" in example_input:
                return CSVHandler.CsvHandler.parse_input(example_input)
            case _ if "json" in example_input:
                return JSONHandler.JSONHandler.parse_input(example_input)
            case _ if "pdf" in example_input:
                return PDFHandler.PdfHandler.parse_input(example_input)
            case _:
                print("File type unknown.")
                return []