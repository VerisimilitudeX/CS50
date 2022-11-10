from cs50 import get_int

# Prompt the user for the credit card number (assume that the user enters only a number)
number = get_int("Number: ")

# Store the first 1 and 2 digits of the credit card number entered
beginning2 = int(str(number)[:2])
beginning1 = int(str(number)[:1])

# Check if the credit card is valid
if (not (beginning2 == 34 or beginning2 == 37 or beginning1 == 4 or beginning1 == 5 or beginning1 == 6)):
    print("INVALID")
    exit()

# Vars
product = 0
everyotherdig = []
others = []

# Add 2 times the digit at every alternate index starting from the second last
index = len(str(number)) - 2
for j in range(index, -2, -1):
    if (index - j) % 2 == 0:
        dig = int(str(number)[j])
        everyotherdig.append(dig * 2)
    # If the number wasn't multiplied by 2, add to another list (this will be useful later)
    else:
        others.append(int(str(number)[j]))

# Split numbers that are 2 digits into 2 numbers
for i in range(len(everyotherdig)):
    if len(str(everyotherdig[i])) == 2:
        everyotherdig.append(int(str(everyotherdig[i])[0]))
        everyotherdig.append(int(str(everyotherdig[i])[1]))
        everyotherdig.pop(i)

# Add all the numbers in the list together
sumdigits = 0
for i in range(len(everyotherdig)):
    sumdigits += everyotherdig[i]

# Add that sum to the digits that weren't multiplied by 2
othersum = 0
for i in range(len(others)):
    othersum += others[i]

finalsum = sumdigits + othersum

# Check if the last digit in the sum is 0
valid = True
lastdigit = int(str(finalsum)[len(str(finalsum)) - 1])

if lastdigit == 0:
    # If yes, then the credit card number passes the checksum
    valid = True
elif lastdigit != 0:
    valid = True

# If the card is valid, then find which company made it
if valid == True and len(str(number)) >= 13:
    # Check if it is an American Express card
    if beginning2 == 34 or beginning2 == 37:
        print("AMEX")
        exit()
    # Check if it is a MasterCard
    elif beginning2 == 51 or beginning2 == 52 or beginning2 == 53 or beginning2 == 54 or beginning2 == 55:
        print("MASTERCARD")
        exit()
    # Check if it is a Visa card
    elif beginning1 == 4:
        print("VISA")
        exit()
    else:
        print("INVALID")
        exit()

print("INVALID")
