/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if(n < 0) {
        return false;
    }
    
    int start = 0;
    int end = n;
    //int middle = (start + end) / 2;
    
    while(start <= end) {
        int middle = (start + end) / 2;
        if(values[middle] < value) {
            start = middle + 1;
        } else if(value == values[middle]) {
            return true;
            
        } else {
            end = middle - 1;
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int dummy = 0;
    int swap = -1;
    
    while(swap != 0) {
        swap = 0;
        for(int i = 0; i < n; i++) {
            if(values[i] > values[i+1]) {
                dummy = values[i+1];
                values[i+1] = values[i];
                values[i] = dummy;
                swap++;
            }
        }   
    }
    
}