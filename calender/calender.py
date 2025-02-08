# 1. Name:
#      -Michael Johnson
# 2. Assignment Name:
#      Lab 03: Calendar
# 3. Assignment Description:
#      This program will take a users input, a month and a year, and as long as it follows the rules a formated calander will be shown in the terminal. 
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part of this assignment for me was dealing with the input validation and ensuring the program handled edge cases properly. 
#      I needed to make sure that the program would only accept valid inputs for both the month and the year while also providing meaningful 
#      feedback to the user when the input was incorrect. It was a bit tricky to structure the loops without using break or continue, especially 
#      when I had to make sure the program would keep prompting the user until the input was valid. I had to find a way to ensure that the input 
#      was properly validated without making the code overly complicated or difficult to follow.
# 5. How long did it take for you to complete the assignment?
#      This took me about 3 hours, from reading the intructions, converting my structure chart to code, and doing the test cases. 



from dataclasses import dataclass
import os
from time import sleep

#create data class for month
@dataclass
class Month:
    name: str
    days: int

# dictionary to hold month number, name, and day count
months = {
    1: Month("January", 31),
    2: Month("February", 28),  # this will change if there is a leap year, 28 or 29 days
    3: Month("March", 31),
    4: Month("April", 30),
    5: Month("May", 31),
    6: Month("June", 30),
    7: Month("July", 31),
    8: Month("August", 31),
    9: Month("September", 30),
    10: Month("October", 31),
    11: Month("November", 30),
    12: Month("December", 31),
}

# this function will check if the year is a leap year, and then return true or false to be used later
def is_leap_year(year):
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

# this calculates the days since January 1, 1753, since that is the earlies the program will go, we can reference it.
def calculate_days_since_1753(month, year):
    # adjust february if it was a leap year
    if is_leap_year(year):
        months[2].days = 29
    else:
        months[2].days = 28

    total_days = 0

    # go through each year between 1753 and input year and add the days
    # this will account for leap years as well
    for y in range(1753, year):
        total_days += 365
        if is_leap_year(y):
            total_days += 1

    # go through and add the days for the months of the current year up to the target month
    for m in range(1, month):
        total_days += months[m].days

    return total_days, months[month].days

# this function will compute the day of the week (0 = Sunday, 6 = Saturday)
def compute_offset(month, year):
    total_days, _ = calculate_days_since_1753(month, year)
    # January 1, 1753 was a Monday, which corresponds to day 1
    day_of_week = (total_days + 1) % 7  # 1 because Jan 1, 1753 is Monday (day 1)
    return day_of_week

# this functino will format our calender for displaying based on input month and year
def display_table(month, year, num_days, dow):
    # create the table header with month and year
    month_name = months[month].name
    print("")
    print(f"Calendar for {month_name}, {year}")
    print("")
    print(" Su  Mo  Tu  We  Th  Fr  Sa")

    # print leading spaces for the first week if dow is not zero
    for _ in range(dow):
        print("    ", end="")

    # print the days of the month
    for dom in range(1, num_days + 1):
        # print day number with consistent width, so they are aligned properly
        print(f"{dom:>3}", end=" ")

        # increment the day of the week (dow)
        dow += 1

        # if we reach the end of the week (Saturday), move to the next line
        if dow % 7 == 0:
            print()

    # Ensure the last line is complete if necessary
    if dow % 7 != 0:
        print()  # Print a newline if the last row is incomplete
    print("")

def main():
    # Get valid month input (1-12)
    os.system('cls')
    month = 0
    while month < 1 or month > 12:
        try:
            month = int(input("Enter a Month (1-12): "))
            if month < 1 or month > 12:
                os.system('cls')
                print("ERROR: Month must be between 1 and 12.")
                sleep(1)
        except ValueError:
            os.system('cls')
            print("ERROR: Month must be an integer.")
            sleep(1)

    # Get valid year input (>= 1753)
    os.system('cls')
    year = 0
    while year < 1753:
        try:
            year = int(input("Enter a Year (1753 or Later): "))
            if year < 1753:
                os.system('cls')
                print("ERROR: Year must be 1753 or later.")
                sleep(1)
        except ValueError:
            os.system('cls')
            print("ERROR: Year must be an integer.")
            sleep(1)

    # Get the starting day of the week for the 1st of the month
    dow = compute_offset(month, year)

    # Get the number of days in the month
    _, num_days = calculate_days_since_1753(month, year)
    
    os.system('cls')
    # Display the calendar table
    display_table(month, year, num_days, dow)

# Run the program
if __name__ == "__main__":
    main()
