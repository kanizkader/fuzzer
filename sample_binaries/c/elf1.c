#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <elf.h>

#define BUFFER_SIZE 1024

int main() {
    unsigned char buffer[BUFFER_SIZE];
    size_t bytesRead;
    Elf64_Ehdr *header;

    bytesRead = fread(buffer, 1, BUFFER_SIZE, stdin);

    if (bytesRead < sizeof(Elf64_Ehdr)) {
        printf("Error: Input too small to be a valid ELF file.\n");
        return 1;
    }

    header = (Elf64_Ehdr *)buffer;

    // Check if it's an ELF file
    if (memcmp(header->e_ident, ELFMAG, SELFMAG) != 0) {
        printf("Not an ELF file.\n");
        return 1;
    }

    // Vulnerable code: Fixed-size array for section headers
    Elf64_Shdr sections[10];

    // Read section headers without proper bounds (mutated section headers can overflow)
    if (header->e_shoff + header->e_shnum * sizeof(Elf64_Shdr) > BUFFER_SIZE) {
        printf("Error: Section headers exceed buffer size.\n");
        return 1;
    }

    memcpy(sections, buffer + header->e_shoff, header->e_shnum * sizeof(Elf64_Shdr));

    printf("Number of section headers: %d\n", header->e_shnum);

    return 0;
}