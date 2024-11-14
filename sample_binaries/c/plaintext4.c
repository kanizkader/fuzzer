#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 128

int main(int argc, char *argv[]) {
    char buffer[BUFFER_SIZE];

    fread(buffer, sizeof(char), 512, stdin); // vuln in fread

    printf("Printing contents:\n%s\n", buffer);
    return 0;
}