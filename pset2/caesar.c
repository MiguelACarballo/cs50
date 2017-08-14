#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) {
    if(argc != 2) {
        return 1;
    } else {
        int key = atoi(argv[1]);
        
        printf("plaintext: ");
        string text = get_string();
        
        for(int i = 0; i < strlen(text); i++) {
            // check for alphabetical character
            if(isalpha(text[i])) {
                // check for uppercase letter
                if(isupper(text[i])) {
                    text[i] = (((text[i] + key) - 65) % 26) + 65;
                }
                // check for lowercase letter
                if(islower(text[i])) {
                    text[i] = (((text[i] + key) - 97) % 26) + 97;
                }
            }
        }
        printf("ciphertext: %s\n", text);
    }
    return 0;
}
