#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* getTextFromFile(char* filename) {
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("Something went wrong opening and reading the file (Error %d)\n", errno);
        exit(EXIT_FAILURE);
    }
    
    // Create buffer with the cyphertext
    char buffer[256] = {0};
    int readSuccess = fscanf(fp, "%s\n", buffer);
    if (!readSuccess) {
        printf("Failure reading from file (error %d)\n", errno);
        exit(EXIT_FAILURE);
    }

    int bSize = strlen(&buffer[0]);
    char* text = (char*) calloc(bSize + 1, sizeof(char));
    memcpy(text, buffer, bSize);
    return text;
}
