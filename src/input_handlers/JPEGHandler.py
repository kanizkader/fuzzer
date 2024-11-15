import random
from PIL import Image
from PIL import JpegImagePlugin
import io

class JPEGHandler:

    @staticmethod
    def image_to_bytes(img):
        """
        Converts a PIL Image to a byte array
        """
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')  # Save to the byte array in JPEG format
        return img_byte_arr.getvalue()  # Get the raw byte data

    @staticmethod
    def bad_strings():
        bad_string_options = []
        with open('./src/input_handlers/bad-strings.txt', 'r') as bad_strings:
            for bad_string in bad_strings:
                if not bad_string.startswith(('#', '\n')):
                    bad_string_options.append(bad_string.strip('\n'))
        return bad_string_options
    
    @staticmethod
    def append_strings(base_input, bad_strings):
        """
        Appends bad strings directly to the end of the image byte array
        """
        fuzzed = []
        for string in bad_strings:
            fuzzed.append(base_input + string.encode())
        
        fuzzed.append(base_input + ('a' * 100000).encode())
        return fuzzed

    @staticmethod
    def append_image(base_input):
        """
        Appends an image to the end of the given byte array
        """
        width, height = 500, 500
        image = Image.new('RGB', (width, height), color='white')
        img_bytes = JPEGHandler.image_to_bytes(image)
        return [base_input + img_bytes]

    @staticmethod
    def buffer_overflow(image, scale_factor):
        """
        Resizes the image to the scale factor and returns a byte array
        """
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_img = image.resize((new_width, new_height), Image.LANCZOS)

        return JPEGHandler.image_to_bytes(resized_img)

    @staticmethod
    def include_strings(base_input, bad_strings):
        """
        Appends bad strings before the end of the image byte array
        so they are considered part of the image
        """
        eoi_pos = base_input.rfind(b'\xFF\xD9')
        fuzzed = []

        if eoi_pos != -1:
            for string in bad_strings:
                new_input = base_input[:eoi_pos] + str(string).encode() + b'\xFF\xD9'
                fuzzed.append(new_input)

        return fuzzed

    @staticmethod
    def mutate(base_input):        
        fuzzed = []

        bad_strings = JPEGHandler.bad_strings()
        
        fuzzed += JPEGHandler.append_strings(base_input, bad_strings)
        fuzzed += JPEGHandler.append_image(base_input)
        fuzzed += JPEGHandler.include_strings(base_input, bad_strings)
        
        return fuzzed
    
    @staticmethod
    def parse_input(base_input):
        """
        Returns inputs to the harness.
        """
        return JPEGHandler.mutate(base_input)
    
    @staticmethod
    def send_jpeg():
        return "jpeg"