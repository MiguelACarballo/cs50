#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) {
    if(argc != 2) {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    
    printf("%i\n", argc);
    printf("%s\n", argv[1]);
    string key_string = argv[1];
    
    // rejection of non-alpha keywords
    for(int i = 0; i < strlen(argv[1]); i++) {
        if(!isalpha(key_string[i])) {
            printf("Usage: ./vihgenere k\n");
            return 1;
        }
    }
        
    printf("plaintext: ");
    string text = get_string();
    int check_key = 0; // index of key
    
    for(int i = 0; i < strlen(text); i++) {
        // check for alphabetical character
        if(isalpha(text[i])) {
            int key = toupper(key_string[check_key]) - 65;
            if(key == -65){
                key += 65;
            }
            // check for uppercase letter
            if(isupper(text[i])) {
                text[i] = (((text[i] + key) - 65) % 26) + 65;
            }
            // check for lowercase letter
            if(islower(text[i])) {
                text[i] = (((text[i] + key) - 97) % 26) + 97;
            }
                
            // increment check_key
            check_key++;
            
            if(check_key > strlen(key_string) -1) {
                check_key = 0;
            }
        }
    }
    printf("ciphertext: %s\n", text);
    return 0;
}
