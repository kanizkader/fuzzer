# General
### Running the Fuzzer
To run the fuzzer, you only need to use the following command in your terminal to trigger the shell script:
```
./run_fuzzer
```
This script will pull in the `binaries/` and `example_inputs/` folders to the environment the same way that you see it when you are developing. The output will be saved to `fuzzer_output/` folder. *This is the same shell script that will be run by the tutors.*

### Adding Dependencies
If you need to add dependencies to the project, you can do so by editing the `requirements.txt` file. Just add the name of the package you need on a new line in the file (optionally mention the version you need too e.g. `somepackage==69.420`).

Note: Please don't add unnecessary dependencies. It's gonna make the build process slow and then Adam will be sad and give us 0.

### Adding Input Handlers
When you need to add input handlers to the project, you can do so by editing the `input_handlers.py` file. Add a new class to the file with the name of the input handler you need.

### Adding Binaries
If you need to add binaries to the project, you can do so by adding them to the `binaries` folder. Please make sure to also add a corresponding example input file to the `example_inputs` folder so that we all code solutions properly. The fuzzer will automatically pull them into the docker container when you run the fuzzer.

# Fuzzer Functionality

TODO

## Mutation Strategies

### Basic
- Bit Flips: Not Implemented
- Byte Flips: Not Implemented
- Known Ints: Not Implemented

### Intermediate
- Repeated Parts: Not Implemented  
- Keyword Extraction: Not Implemented
- Arithmetic: Not Implemented

### Advanced
- Coverage-based mutations: Not Implemented 

## File Formats

### Basic
- CSV: Implemented
- JSON: Implemented 
- XML: Not Implemented  

### Intermediate
- JPEG: Not Implemented 
- ELF: Not Implemented  

### Advanced
- PDF: Not Implemented   

# Harness
TODO