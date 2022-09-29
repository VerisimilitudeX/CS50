#include <stdio.h>

#include <cs50.h>

#include <string.h>

#include <stdlib.h>

#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int k = atoi(argv[1]);
    if (k < 0)
    {
        printf("Usage: ./caesar key\n");
        return 2;
    }

    string text = get_string("Text: ");

    printf("ciphertext: ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                char cipher_num_capital = ((text[i] - 65 + k) % 26) + 65;
                printf("%c", cipher_num_capital);
            }

            if (islower(text[i]))
            {
                char cipher_num_small = ((text[i] - 97 + k) % 26) + 97;
                printf("%c", cipher_num_small);
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }

    printf("\n");
    return 0;
}