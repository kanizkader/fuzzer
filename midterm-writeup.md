# Fuzzy Documentation
## Overview
The fuzzer at this stage tackles CSV and JSON input types and does basic mutations. It primarily uses a list of known bad strings (e.g. format string, directory traversal characters) that it cycles through and creates a list of mutated inputs to try. Each class implements a few strategies independently at this stage. We will combine the logic from both of the handlers when we move onto more advanced strategies for the rest of the project.
## Current Functionality
### File Format Support
CSV: Currently implemented with schema analysis and the following strategies:
* Empty strings, empty tables
* Buffer overflow strategies (many rows, many columns, long cell contents)
* Byte flips 
* Known bad strings

JSON: Currently implemented with the following strategies:
* Trigger a fixed length buffer overflow
* Byte flips
* Known bad strings
### Harness Functionality
* Executes and passes input to each binary using subprocess.run()
* Captures stdout, stderr, and a number of exit codes during execution
* Writes vulnerable inputs that work to fuzzer_output directory
### Bug Detection Capabilities
* Buffer overflows
* Format string vulnerabilities
* Segmentation faults, program crashes
## Suggested Improvements
We want to look to add in code coverage tracking later in the project and also look to make our mutation strategies more advanced. We can do this by looking at the current crashes and mutating those as well. We want our mutations to be informed by how the program behaves to different inputs since currently it only logs when it breaks something. We also want to expand our bug detection capabilities to detect non-standard behaviour that doesn’t necessarily cause a crash e.g. unauthorised memory access. We were unable to detect a crash for the csv1 and json2 binary at this stage and hope that more advanced methods will allow us to find one.
