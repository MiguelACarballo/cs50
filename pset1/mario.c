#include <stdio.h>
#include <cs50.h>

int main(void) {
    int height;
    int spaces;
    int hashes;
    
    do{
        printf("Height: ");
        height = get_int();
    } while(height < 0 || height > 23);
    
    for(int i = 0; i < height; i++) {
        
        for(spaces = height - i; spaces > 1; spaces--) {
            printf(" ");
        }
        
        for(hashes = 0; hashes <= i + 1; hashes++) {
            printf("#");
        }
        
        printf("\n");
    }
}