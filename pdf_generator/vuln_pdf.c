// NOTE: THIS IS CHATGPT GENERATED FOR THE SAKE OF TESTING
// NEED TO RE_WRITE !!!!
// RUN USING ./vuln_pdf < vuln_pdf.txt

#include <stdio.h>
#include <stdlib.h>

void read_pdf(const char *filename) {
    FILE *file = fopen(filename, "rb");  // Open the PDF file in binary mode
    if (!file) {
        perror("Failed to open file");
        return;
    }

    // Vulnerable buffer
    unsigned char buffer[64];  // Small buffer for reading PDF data
    size_t bytesRead;

    // Read data into the buffer without checking the size
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        for (size_t i = 0; i < bytesRead; i++) {
            printf("%02X ", buffer[i]);  // Print each byte as hex
        }
        // Here, if the PDF file is large, it could overflow the buffer
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <pdf_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    read_pdf(argv[1]);
    return EXIT_SUCCESS;
}
