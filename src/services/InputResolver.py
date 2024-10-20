import pathlib
from input_handlers import JsonHandler, PDFHandler

class InputResolver:
    """
    Given example input, calls the relevant file type handler and returns the output
    """

    @staticmethod
    def getInput(example_input):
        """
        Calls the required filetype handler
        """
        example_input = example_input.lower()
        match True:
            case _ if "csv" in example_input:
                return JsonHandler.JsonHandler.send_json(example_input)
            case _ if "json" in example_input:
                return PdfHandler.PdfHandler.send_json(example_input)
            case _:
                print("File type unknown.")
                return []