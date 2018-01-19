/**
 * Implements a dictionary's functionality.
 */

 #include <stdbool.h>
 #include <stdlib.h>
 #include <stdio.h>
 #include <string.h>
 #include <ctype.h>
 
 #include "dictionary.h"
 
 #define HASHTABLE_SIZE 71546
 // typedef the struct
 
 typedef struct node {
     char word[LENGTH + 1];
     struct node *next;
 } node;
 
 node *hashTable[HASHTABLE_SIZE] = {NULL};
 
 unsigned int wordCount = 0;
 
 /**
  * Returns true if word is in dictionary else false.
  */
 bool check(const char *word)
 {
     int wordLen = strlen(word);
     char low_word[wordLen + 1];
 
     for (int i = 0; i < wordLen; i++) {
         low_word[i] = tolower(word[i]);
     }
 
     low_word[wordLen] = '\0';
 
     int hashed = hash(low_word);
     node *cursor = hashTable[hashed];
 
     while (cursor != NULL) {
         if(strcmp(cursor->word, low_word) == 0) {
             return true;
         } else {
             cursor = cursor->next;
         }
     }
 
     return false;
 }
 
 /**
  * Loads dictionary into memory. Returns true if successful else false.
  */
 bool load(const char *dictionary)
 {
     FILE *dctFile = fopen(dictionary, "r");
     char* word = malloc((LENGTH + 1) * sizeof(char));
 
     if(dctFile == NULL) {
         fprintf(stderr, "Could not open dictionary.\n");
         return false;
     }
 
     while (true) {
 
         node *new_node = malloc(sizeof(node));
         if(new_node == NULL) {
             unload();
             return false;
         }
         fscanf(dctFile, "%s", word);
         if(feof(dctFile) != 0) {
             free(word);
             free(new_node);
             break;
         }
         strcpy(new_node->word, word);
 
         int hashIndex = hash(word);
 
         if (hashTable[hashIndex] == NULL) {
             hashTable[hashIndex] = new_node;
             new_node->next = NULL;
         } else {
             new_node->next = hashTable[hashIndex];
             hashTable[hashIndex] = new_node;
         }
 
         wordCount++;
     }
 
     fclose(dctFile);
     return true;
 }
 
 /**
  * Returns number of words in dictionary if loaded else 0 if not yet loaded.
  */
 unsigned int size(void)
 {
     if(wordCount > 0) {
         return wordCount;
     }
     return 0;
 }
 
 /**
  * Unloads dictionary from memory. Returns true if successful else false.
  */
 bool unload(void)
 {
     for (int i = 0; i < HASHTABLE_SIZE; i++) {
         node *cursor = hashTable[i];
         while (cursor != NULL) {
             node *buffer = cursor;
             cursor = cursor->next;
             free(buffer);
         }
     }
     return true;
 }
 
 unsigned int hash(char *word) {
     unsigned int hash = 0;
     for (int i = 0, n = strlen(word); i < n; i++) {
         hash = (hash * word[0] * i)^word[i];
     }
     return hash % HASHTABLE_SIZE;
 }
 