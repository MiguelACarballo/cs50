/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames and multiplicator
    char *n = argv[1];
    char *infile = argv[2];
    char *outfile = argv[3];
    
    // check if n is between 0 and 100
    int scale = atoi(n);
    
    if(scale < 0 || scale > 100) {
        fprintf(stderr, "n has to be between 0 and 100.\n");
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf_in;
    fread(&bf_in, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi_in;
    fread(&bi_in, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf_in.bfType != 0x4d42 || bf_in.bfOffBits != 54 || bi_in.biSize != 40 || 
        bi_in.biBitCount != 24 || bi_in.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    // outfile's bitmapfileheader
    BITMAPFILEHEADER bf_out = bf_in;
    
    // outfile's bitmapinfoheader
    BITMAPINFOHEADER bi_out = bi_in;
    
    bi_out.biWidth *= scale;
    bi_out.biHeight *= scale;
    
    // determine padding for input scanlines
    int padding_in = (4 - (bi_in.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // determine padding for output scanlines
    int padding_out = (4 - (bi_out.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    bi_out.biSizeImage = (bi_out.biWidth * sizeof(RGBTRIPLE) + padding_out) * abs(bi_out.biHeight);
    bf_out.bfSize = 54 + bi_out.biSizeImage;
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_out, sizeof(BITMAPFILEHEADER), 1, outptr);
    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_out, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi_in.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for(int vertical = 0; vertical < scale; vertical++) {
            fseek(inptr, sizeof(BITMAPFILEHEADER) + sizeof (BITMAPINFOHEADER) + (i * (biHeight * sizeof(RGBTRIPLE) + padding_in)), SEEK_SET);
            for (int j = 0; j < bi_in.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
        
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                    
                // write RGB triple to outfile
                for(int k = 0; k < scale; k++)
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        
            // skip over padding, if any
            fseek(inptr, padding_in, SEEK_CUR);
        
            // then add it back (to demonstrate how)
            for (int k = 0; k < padding_out; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
