# Start from a default ubuntu image.
FROM ubuntu:22.04

# Install Python and pip
RUN apt update && apt install -y python3 python3-pip

# Copy the requirements file
COPY requirements.txt /

# Install the dependencies
RUN pip install -r /requirements.txt

# Copy entire directory to container
COPY . .

# Run it.
CMD ["python3", "src/fuzzer.py"]
