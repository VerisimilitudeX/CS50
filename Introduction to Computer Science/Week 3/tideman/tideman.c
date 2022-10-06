// import libraries
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
void swap(int a, int b);
bool circle(int a, int b);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Iterate over the candidate count
    for (int x = 0; x < candidate_count; x++)
    {
        // If it matches the candidate's name
        if (strcmp(name, candidates[x]) == 0)
        {
            // updates the rank for that candidate and exits
            ranks[rank] = x;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    printf("%i, %i, %i\n", ranks[0], ranks[1], ranks[2]); // for B A C = 1, 0, 2
    for (int x = 0; x < candidate_count - 1; x++)
    {
        for (int y = (x + 1); y < candidate_count; y++)
        {
            preferences[(ranks[x])][(ranks[y])]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int p = 0;
    for (int y = 0; y < candidate_count; y++)
    {
        for (int z = 0; z < candidate_count; z++)
        {
            if (preferences[y][z] > preferences[z][y])
            {
                pairs[p].winner = y;
                pairs[p].loser = z;
                pair_count++;
                p++;
            }
        }
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    printf("%iprefstart0\n", preferences[pairs[0].winner][pairs[0].loser]);
    printf("%iprefstart1\n", preferences[pairs[1].winner][pairs[1].loser]);
    printf("%iprefstart2\n", preferences[pairs[2].winner][pairs[2].loser]);
    int count = 0;
    int place = 0;
    for (int y = 0; y < pair_count; y++)
    {
        for (int z = 0; z < pair_count; z++)
        {
            if (preferences[pairs[y].winner][pairs[y].loser] > preferences[pairs[z].winner][pairs[z].loser])
            {
                count++;
            }
        }
        if (count == pair_count - (place + 1))
        {
            swap(place, y);
            place++;
        }
        count = 0;
    }

    printf("%iprefend0\n", preferences[pairs[0].winner][pairs[0].loser]);
    printf("%iprefend1\n", preferences[pairs[1].winner][pairs[1].loser]);
    printf("%iprefend2\n", preferences[pairs[2].winner][pairs[2].loser]);
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int x = 0; x < pair_count; x++)
    {
        if (!circle(pairs[x].winner, pairs[x].loser)) // if no cycle created then lock pair x
        {
            locked[pairs[x].winner][pairs[x].loser] = true;
        }
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    // look for a candidate that was never locked in as a loser
    for (int x = 0; x < candidate_count; x++)
    {
        bool neverloser = true;

        for (int y = 0; y < candidate_count; y++)
        {
            // check to see if winner is ever loser
            if (locked[y][x] == true)
            {
                neverloser = false;
            }
        }
        // if never loser then winner
        if (neverloser == true)
        {
            printf("%s\n", candidates[x]);
            break;
        }
    }

    return;
}

void swap(int a, int b)
{
    pair temp = pairs[a];
    pairs[a] = pairs[b];
    pairs[b] = temp;
    return;
}

bool circle(int a, int b)
{
    if (locked[b][a] == true)
    {
        return true;
    }
    for (int x = 0; x < pair_count; x++)
    {
        if (locked[x][a] == true)
        {
            return circle(x, b);
        }
    }
    return false;
}