#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void) {
    float owed;
    int count = 0;
    int round_owed;
    
    printf("O hai! How much change is owed?\n");
    owed = get_float();
    while(owed < 0){
        printf("How much change is owed?\n");
        owed = get_float();
    }
    round_owed = round(owed * 100);
    
    while(round_owed / 25 > 0) {
        round_owed -= 25;
        count++;
    }
    
    while(round_owed / 10 > 0) {
        round_owed -= 10;
        count++;
    }
    
    while(round_owed / 5 > 0) {
        round_owed -= 5;
        count++;
    }
    
    while(round_owed / 1 > 0) {
        round_owed -= 1;
        count++;
    }
    printf("%i\n", count);
}