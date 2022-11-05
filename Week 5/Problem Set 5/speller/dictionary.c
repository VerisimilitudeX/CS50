// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// make count_words a global variable
// it may be called in size();
unsigned int count_words = 0;

// Prototypes
unsigned int size(void);

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
// N = 26 this is A to Z
const unsigned int N = 20000;

// Hash table
// a hash table is an array of linked lists
node *table[N]; // * points to the first address

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // traverse the linked list searching for a matching word
    // word index position
    int word_index = hash(word);

    // initialize cursor to first node in the linked list
    // note cursor->word is current word
    // note cursor->next is a pointer to the next node address
    node *cursor = table[word_index];

    // while loop to iterate until NULL
    // NULL is the one with no pointer
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true; // word is found
        }
        // set the cursor to the next node in the linked list
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // consider a function on each character in a word to insurace uniqueness however will output fit in N-1?
    // to fit N do module % N
    // output is the address in the linked list
    // return toupper(word[0]) - 'A';

    // new hash function
    // loop over each character in the string
    // square the uppe case ASCII number, sum each squared ASCII number and mod N
    // mid word perform another function
    unsigned int roll_sum = 0;
    unsigned int squared = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        squared = pow(toupper(word[i]), 2);
        if (i == round(strlen(word) / 2))
        {
            roll_sum = roll_sum + round(sqrt(roll_sum)) + 17;
        }
        roll_sum = squared + roll_sum + 47;
    }
    return roll_sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // add a method to sum the words as loading into dictionary
    // Open the dictionary file
    FILE *dict_open = fopen(dictionary, "r"); // pointer to the memory address of the input file
    // printf("pointer to memory address of the memory card %p \n", input_memory_card);
    if (dict_open == NULL)
    {
        printf("Could not open the dictionary file.\n");
        return false;
    }
    else if (dict_open != NULL)
    {
        char buffer[LENGTH + 1];
        int hash_index = 0;
        while (fscanf(dict_open, "%s", buffer) != EOF)
        {
            // printf("yee %s \n",buffer);

            // Create a new node for the word the size of the node
            // enough bytes for the word itselt and the address
            node *n = malloc(sizeof(node));
            // check that the memory initialized ok
            if (n == NULL)
            {
                return false;
                break;
            }
            else if (n != NULL)
            {
                // copy the word into the word portion of the node
                strcpy(n->word, buffer);
                // set address to NULL
                n->next = NULL;

                // testing the hash function
                // printf("testing hash function %i \n", hash(buffer));

                // get the hash number
                hash_index = hash(buffer);

                // case 1 - the first entry
                // if nothing is there equal the first entry to the new node
                if (table[hash_index] == NULL)
                {
                    table[hash_index] = n;
                }
                // case 2 - an entry already exists
                // inserts at the front of the linked list each time
                else if (table[hash_index] != NULL)
                {
                    // set the new node address to the first element index position
                    n->next = table[hash_index];
                    // set the head of the linked list to the previously inserted node
                    table[hash_index] = n;
                }

                // count words
                count_words++;
            }
        } // end while loop
        fclose(dict_open);
        return true;
    }
    else
    {
        return false;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // summed count words whilst loading
    return count_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // tmp and curosr method move cursor->cursor->next. free temp.. cursor->next...NULL
    // loop along the index positions
    for (int i = 0; i < N; i++)
    {
        // set temp and cursor to first index position
        node *temp = table[i];
        node *cursor = table[i];

        // at each index position
        // traverse the linked list at that index position and free - use temp/cursor
        // while loop until NULL
        // at that point next i will begin
        while (temp != NULL)
        {
            // set cursor to next
            cursor = cursor->next; // i+1
            free(temp);
            temp = cursor;
        }
    }
    return true;
}