# Function to check if a year is a leap year
def is_leap_year(year):
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

# Function to calculate the number of days since January 1, 1753
def calculate_days_since_1753(month, year):
    # Days in each month (normal year)
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    # Adjust February for leap year
    if is_leap_year(year):
        days_in_month[2] = 29
    
    total_days = 0
    
    # Add days for each year between 1753 and the given year
    for y in range(1753, year):
        total_days += 365
        if is_leap_year(y):
            total_days += 1
    
    # Add days for the months of the current year up to the target month
    for m in range(1, month):
        total_days += days_in_month[m]
    
    return total_days, days_in_month[month]

# Function to compute the day of the week (0 = Sunday, 6 = Saturday)
def compute_offset(month, year):
    total_days, _ = calculate_days_since_1753(month, year)
    
    # January 1, 1753 was a Monday, which corresponds to day 1
    day_of_week = (total_days + 1) % 7  # 1 because Jan 1, 1753 is Monday (day 1)
    
    return day_of_week

# Function to display the calendar for the given month and year
def display_table(num_days, dow):
    # Table header with proper formatting
    print(" Su  Mo  Tu  We  Th  Fr  Sa ")
    
    # Print leading spaces for the first week if dow is not zero
    for i in range(dow):
        print("   ", end="")

    # Print the days of the month
    for dom in range(1, num_days + 1):
        # Print day number with consistent width
        print(f"{dom:3}", end=" ")
        
        # Increment the day of the week (dow)
        dow += 1
        
        # If we reach the end of the week (Saturday), move to the next line
        if dow % 7 == 0:
            print()  # Start a new line after Saturday
            dow = 0  # Reset dow to Sunday
    
    # Ensure the last line is complete if necessary
    if dow != 0:
        print()



# Main function to take user input and display the calendar
def main():
    # Get valid month input
    while True:
        try:
            month = int(input("Enter the month number: "))
            if month < 1 or month > 12:
                print("Month must be between 1 and 12.")
            else:
                break
        except ValueError:
            print("Month must be an integer and between 1 and 12.")

    # Get valid year input
    while True:
        try:
            year = int(input("Enter year: "))
            if year < 1753:
                print("Year must be 1753 or later.")
            else:
                break
        except ValueError:
            print("Year must be an integer.")
    
    # Get the starting day of the week for the 1st of the month
    dow = compute_offset(month, year)
    
    # Get the number of days in the month
    _, num_days = calculate_days_since_1753(month, year)
    
    # Display the calendar table
    display_table(num_days, dow)

# Run the program
if __name__ == "__main__":
    main()
