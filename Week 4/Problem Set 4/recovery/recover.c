#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 512

int main(void)
{
    FILE *input = fopen("card.raw", "r");
    if (input == NULL | input == 0)
    {
        printf("Could not open card.raw.\n");
        return 1;
    }

    else if (input != NULL)
    {
        unsigned char buffer[BUFFER_SIZE];
        int filecount = 0;
        FILE *picture = NULL;
        int jpg_found = 0;

        while (fread(buffer, BUFFER_SIZE, 1, input) == 1)
        {
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
            {
                if (jpg_found == 1)
                {
                    fclose(picture);
                }
                else
                {
                    jpg_found = 1;
                }

                char filename[8];
                sprintf(filename, "%03d.jpg", filecount);
                picture = fopen(filename, "a");
                filecount++;
            }

            if (jpg_found == 1)
            {
                fwrite(&buffer, BUFFER_SIZE, 1, picture);
            }
        }

        fclose(input);
        fclose(picture);
        return 0;
    }

    return 1;
}