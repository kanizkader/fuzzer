#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 128

int main(int argc, char *argv[]) {
    char buffer[BUFFER_SIZE];

    fread(buffer, sizeof(char), BUFFER_SIZE - 1, stdin);

    printf("Printing contents:\n");
    printf(buffer); // Format String Vuln
    return 0;
}