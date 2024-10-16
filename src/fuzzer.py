import os
import logging
from input_handlers import json_handler, pdf_handler
# from services import hArNesS

def main():
    output_folder = 'fuzzer_output'
    if not os.path.exists(output_folder):
        print(f"Folder '{output_folder}' does not exist.")
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")
        return
    output_file = os.path.join(output_folder, 'test_output2.txt')
    try:
        with open(output_file, 'w') as f:
            print("Writing to file")
            f.write('Test output\n')
            f.write(json_handler.JsonHandler.send_json() + '\n')
            f.write(pdf_handler.PdfHandler.send_pdf() + '\n')
    except Exception as e:
        logging.error(f"An error occurred while writing to the file: {e}")

if __name__ == '__main__':
    main()
