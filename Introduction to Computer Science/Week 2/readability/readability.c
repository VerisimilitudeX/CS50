#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string input = get_string("Text: ");

    int num_letters = count_letters(input);
    int num_words = count_words(input);
    int num_sentences = count_sentences(input);

    /*
     * printf("%i\n", num_letters);
     * printf("%i\n", num_words);
     * printf("%i\n", num_sentences);
     */

    double L = 100 * ((double) num_letters / (double) num_words);
    double S = 100 * ((double) num_sentences / (double) num_words);

    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int total_letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 97 && text[i] <= 122) || (text[i] >= 65 && text[i] <= 90))
        {
            total_letters++;
        }
    }
    return total_letters;
}

int count_words(string text)
{
    int total_words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32)
        {
            total_words++;
        }
    }
    return total_words;
}

int count_sentences(string text)
{
    int total_sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            total_sentences++;
        }
    }
    return total_sentences;
}