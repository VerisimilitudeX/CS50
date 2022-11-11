import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # TODO: Read database file into a variable
    sequences = []
    dnafile = {}

    # Open the file with the DNA sequences
    with open(sys.argv[1]) as dictfile:
        # For each line in the file
        for index, row in enumerate(dictfile):
            # If we are on the first line
            if index == 0:
                # Get the names of each sequence
                sequences = [
                    sequence for sequence in row.strip().split(",")][1:]
                # Otherwise
            else:
                # Get the name of the DNA sequence
                name = row.strip().split(",")
                # Get the DNA sequence
                dnafile[name[0]] = name[1:]

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txtfile:
        sequence = txtfile.read().replace('\n', '')

    # TODO: Find longest match of each STR in DNA sequence
    # initiate a "result" list to save results from "longest_match"
    # Counting each subsequences in the "sequences" list
    result = [longest_match(sequence, STR) for STR in sequences]

    # TODO: Check database for matching profiles
    # compares "result" list against dnafile{} values
    # leave the program if there is a match, and print key(name) in dnafile{}
    # iterate over the sequences
    for s in dnafile:
        # initialize a variable to count the number of matches
        count = 0

        # iterate over the strings of the sequences
        for j in range(len(dnafile[s])):
            # check if the strings match
            if result[j] == int(dnafile[s][j]):
                # if they do, increase the counter
                count += 1

        # if the counter is equal to the number of sequences
        if count == len(sequences):
            # we have a match, so print the name of the person
            return print(s)

    # otherwise, no match
    return print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
