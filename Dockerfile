# Start from a default ubuntu image.
FROM --platform=linux/amd64 ubuntu:22.04

# Install Python, pip, and stuff for executing C binaries.
RUN apt update && apt install -y python3 python3-pip

# Install dependencies for pwntools
RUN apt install -y python3-dev 
RUN apt install -y git && apt install -y libssl-dev 
RUN apt install -y libffi-dev && apt install -y build-essential

# Copy entire directory to container
COPY . .

# Move read only binaries to an executable folder in container
RUN mkdir ./executables
RUN mv binaries/* ./executables

# Install python dependencies
RUN pip install -r /requirements.txt

# Make all binaries in the executables directory executable
RUN chmod +x /executables/*

# Set shell variables
ENV TERM=xterm
ENV TERMINFO=/etc/terminfo

# Run it.
CMD ["python3", "src/fuzzer.py"]
