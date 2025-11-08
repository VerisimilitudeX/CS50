from cs50 import get_int
import sys

# Prompt for card number
number = get_int("Number: ")
s = str(number)


total = 0
for i, ch in enumerate(s[::-1]):
    d = int(ch)
    if i % 2 == 1:
        d *= 2
        if d > 9:
            d -= 9
    total += d

valid = (total % 10 == 0)


if not valid:
    print("INVALID")
    sys.exit()

length = len(s)
first_two = int(s[:2])
first_one = int(s[0])

if length == 15 and first_two in (34, 37):
    print("AMEX")
elif length == 16 and 51 <= first_two <= 55:
    print("MASTERCARD")
elif length in (13, 16) and first_one == 4:
    print("VISA")
else:
    print("INVALID")
