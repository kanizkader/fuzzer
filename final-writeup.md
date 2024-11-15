## Fuzzer overview

The fuzzer searches subdirectories /binaries and /sample\_inputs for an executable and corresponding valid input. For each binary and sample input pair encountered, the harness:

* Passes the input to the **InputResolver** module. This module attempts to identify the file format (e.g. csv, ELF) using built-in file handling tools such as csv.Sniffer() and json.loads().  
* If a likely file format is found, the InputResolver passes the sample input to the relevant **input handler** located in /src/input\_handlers. Each input handler attempts to parse key features of the input and applies **format-specific mutations**. More detail can be found below.  
* For all files, whether or not a file type can be identified, the InputResolver then appends **format-independent mutations** including bit flips/byte flips and extracted keywords.  
* For each fuzzed input returned, the Harness runs the provided binary as a subprocess, and passes the fuzzed input as raw bytes via Popen.communicate().   
* When the subprocess terminates, the Harness collects the return code and any output to stdout or stderr. If a **non-zero return code is detected**, the Harness assigns a detailed error description and returns this to the Fuzzer module. If the subprocess does not terminate within 10 seconds, this is recorded as a **hang** and treated as a crash.  
* When all inputs have been tried, a summary of fuzzer execution is printed to /fuzzer\_output, including every input which caused a crash.

## Format-specific mutation strategies

**CSV**  
The CSVHandler (CSVHandler.py) module parses key features of the sample csv input: number of rows, columns, and whether a header is present. It then applies the following mutation strategies:

* **Buffer overflow-oriented strategies:** many rows, many columns, and very long cell contents. If a header is present, it is preserved.   
  This attempts to find a buffer overflow vulnerability which would allow an attacker to inject code to the stack, leading to dangerous outcomes such as memory corruption or remote code execution.  
* **Simple integer overflow:** cell contents are replaced with large numbers at common integer boundaries e.g. UINT\_MAX, UINT\_MIN. This is to detect any integer overflow vulnerabilities, which can allow attackers to bypass checks and cause the program to execute unwanted behaviour such as leaking memory or escalate privileges.  
* **Mutations based on schema:** cell contents are modified but the overall structure is preserved. New inputs are generated using a combination of valid cell contents extracted from the sample input, strings obtained from a database of inputs known to trigger common vulnerabilities, and combinations of the two.

**JSON**   
The JSONHandler (JSONHandler.py) utilises the JSON structure to parse and mutate inputs. It uses the help of JSONHelper to create a variety of mutations. The following mutation strategies have been implemented:

* **Buffer overflow-oriented strategies:** replacing keys with a lot of contents, replacing values with a lot of contents.   
  This attempts to find a buffer overflow vulnerability which would allow an attacker to inject code into the stack. Found in **JSONHelper.simple\_buffer\_overflow()**  
* **Format string-oriented strategies:** appended format strings to the original values.   
  This attempts to find a format string vulnerability which would allow an attacker to write to different areas of the program. Found in **JSONHelper.put\_format\_str()**  
* **Arithmetic-oriented strategies:** integer underflows, integer overflows have been applied to any integer inputs. This is to detect any integer overflow vulnerabilities, which can allow attackers to bypass checks and cause the program to execute unwanted behaviour such as leaking memory or escalate privileges. Found in **JSONHelper.int\_overflow()** and **int\_underflow()**  
* **Structure:** Malformed JSON by removing curly braces. This can cause some programs to misread the input type and crash due to unexpected input.


**General Plaintext**  
The PlaintextHandler (PlaintextHandler.py) aims for the general plaintext stdin files. Similar to the previous two, it applies the following strategies:

* **Buffer overflow-oriented strategies:** using pwn.cyclic to generate a series of increasingly long payloads. Found in **PlaintextHelper.simple\_buffer\_overflow()**  
  This attempts to find a buffer overflow vulnerability which would allow an attacker to inject code into the stack.  
* **Format string-oriented strategies:** appended format strings to the original values.  
  This attempts to find a format string vulnerability which would allow an attacker to write to different areas of the program. Found in **PlaintextHelper.put\_format\_str()**

**XML**  
The XMLHandler (XMLHandler.py) targets XML files with the following strategies:

* **Buffer overflow-oriented strategies:** replaces tag properties and tag content from the example input with long strings and large numbers and parses large xml files with deeply nested tags. Found in **buffer\_overflow()**  
  This attempts to find a buffer overflow vulnerability which would allow an attacker to inject code into the stack.  
* **Structure and bad XML:** open tags with no closing tags, commonly unaccepted input such as undefined and null, and non-xml input such as strings. Found in **sub\_bad\_strings()**  
  This attempts to crash the program, however, is unlikely to have a large impact unless paired with a different exploit.  
* **Format string-oriented strategies:** replaces tag properties and content in the example input with common format string attacks such as “%p” and “%n”. Found in **sub\_bad\_strings()**  
  This attempts to find a format string vulnerability which would allow an attacker to write to different areas of the program. 

**JPEG**  
The JPEG Handler (JPEGHandler.py) applies the following strategies to JPEG files:

* **File input corruption:** involving appending long or commonly problematic strings of bytes directly to the end of the JPEG file. Found in **append\_strings**() and **append\_image**()  
  Although unlikely to have an effect on the program’s buffer due to being added after the End of Input tag in the image, it could cause some programs to misread the file type or crash from the unexpected input.  
* **JPEG injection:** involving injecting large amounts of bad bytes within the image before the End of Input tag. Found in **include\_image**()  
  This corrupts the strict image format and impacts metadata, causing programs to not be able to read the image properly and potentially execute malware.

**ELF**  
The ELF handler (ELFHandler.py) is currently relying on the valid input example to generate mutations.

* **ELF Header**: file identification fields are modified, including the file type (e\_type) and target architecture (e\_machine), to test various executable types and trigger parsing errors or architecture-specific handling.  
* **Section Header Mutations**: The section header table entries are altered, randomising section types and flags, which can influence binary loader interpretation and trigger parsing failures or security checks.  
* **Random Section Mutations**: byte flips are applied to key sections like .text, .data, .rodata, and .bss, potentially causing runtime crashes or unexpected behaviour, with a cap of 40 mutations per file for testing efficiency.

**PDF**  
The PDFHandler (PDFHandler.py) aims for the PDF stdin. Similar to the plaintext strategies, it applies the following strategies: 

* **Buffer overflow-oriented strategies:** using pwn.cyclic to generate a series of increasingly long payloads. Found in **PDFHelper.simple\_buffer\_overflow()**  
  This attempts to find a buffer overflow vulnerability which would allow an attacker to inject code into the stack.  
* **Format string-oriented strategies:** appended format strings to the original values.  
  This attempts to find a format string vulnerability which would allow an attacker to write to different areas of the program. Found in **PDFHelper.put\_format\_str()**

## Format-independent mutation strategies

The following mutation strategies are used for all binaries, regardless of valid input format:

* **Simple empty strings:** empty input can cause issues if the program is not equipped to handle it. e.g. a single null byte, new line character, carriage return, etc.  
* **Bit flips/byte flips**: the MutationHelper module randomly applies a bitmask to approximately 6% of bytes in the sample input file. This is done multiple times for every input. A seed is used to ensure that this process is deterministic and repeatable.  
  Bit/byte flips can cause the program to crash or act unexpectedly, creating an avenue for further attacks.  
* **Keyword extraction:** The class is designed to extract readable text, and then applies various filters to identify interesting keywords. It specifically looks for common keywords for credentials etc. (loaded from a predefined list), source code file references (.c, .h, .o files), meaningful strings (filtering out random junk). The findings are given directly at the end of the program to let the fuzz boy or fuzz girl better align their attack to the target binary.  
* **Bad strings:** strings known to trigger common vulnerabilities (e.g. format strings, non-ASCII characters, large inputs for buffer overflows) are inserted into all text-based inputs. These are based on a [list of common exploits](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/big-list-of-naughty-strings.txt) and stored in a database called ‘bad-strings.txt’.

## Vulnerability detection

We have tested our fuzzer against the provided binaries as well as some self-written test binaries, and have been successful in detecting buffer overflows, integer overflows and format string vulnerabilities. These self-written binaries can be found in our \`sample\_binaries\` folder.

## Improvements

Our fuzzer currently detects a crash by viewing the process return code and standard error output. We investigated but ultimately were unable to implement any advanced detection strategies such as using [Electric Fence](https://linux.die.net/man/3/efence) to detect unusual memory access that did not result in a crash, or attaching the program to a debugger to collect detailed crash stats. This would be a key area for improvement if our fuzzer is to detect more complex, real-world bugs.

Our fuzzer also does not have any means to detect program coverage. We investigated using gdb’s Python API to run the program and apply breakpoints at every function call using rbreak, but were unable to implement it reliably enough. In future, we might investigate libraries written in C to achieve this functionality, as there seem to be more options than in Python.

In the JPEG Handler, we attempted to create a buffer overflow vulnerability by inputting very large images, found in **JPEGHandler.buffer\_overflow**() however we weren’t able to get it running. Given more time, we could have looked into vulnerabilities relating compression and decompression, such as an exploit that appears only once the file has been decompressed by the program, or vulnerabilities caused by editing JPEG headers. There were also older JPEG exploits such as the JPEG of Death that triggers a heap overflow that we could have studied and tried replicating. 

In the future it could be possible to improve the lists used for bad strings and keyword mutation to deliver more specific exploits targeting each binary. Additionally, some programs require passwords which we could implement a password list or search the binaries for to break through.  
