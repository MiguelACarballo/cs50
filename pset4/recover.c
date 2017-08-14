#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[]) {
    if(argc != 2) {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *inFile = argv[1];

    FILE *inptr = fopen(inFile, "r");

    if(inptr == NULL) {
        fprintf(stderr, "Could not open file %s\n", inFile);
        return 2;
    }

    int count = 0;
    char outFileName[8];
    int foundPic = 0;
    FILE *outptr = NULL;
    BYTE buffer[512];

    while (fread(buffer, 512, 1, inptr) == 1) {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) {
            if(foundPic == 1) {
                fclose(outptr);
            } else {
                foundPic = 1;
            }
            sprintf(outFileName, "%03d.jpg", count);
            outptr = fopen(outFileName, "a");
            count++;
        }
        if(foundPic == 1) {
            fwrite(&buffer, 512, 1, outptr);
        }
    }
    fclose(inptr);
    fclose(outptr);
    return 0;
}
