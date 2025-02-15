# 1. Name:
#      -Michael Johnson-
# 2. Assignment Name:
#      Lab 05 : Sudoku Draft
# 3. Assignment Description:
#      -This program plays the game of sudoku-
# 4. What was the hardest part? Be as specific as possible.
#      One of the most challenging parts was handling user input validation properly. Ensuring that moves were formatted correctly, 
# numbers were within valid ranges, and the player wasn’t overwriting pre-filled cells required multiple checks. Initially, the program 
# relied on break and continue statements, but I refactored it to use pure conditional logic for cleaner flow.
# 5. How long did it take for you to complete the assignment?
#      -3-


import json
import os
import time

def display_instructions():
    '''
    Displays instructions on how to play the Sudoku game.
    This is shown to the player at the start so they know the rules.
    '''
    print("\n=== Sudoku Instructions ===")
    print("1. Sudoku is played on a 9x9 grid, divided into nine 3x3 subgrids.")
    print("2. Each row, column, and 3x3 subgrid must contain the numbers 1-9 exactly once.")
    print("3. Some numbers are pre-filled as clues; you must fill in the rest correctly.")
    print("4. A number cannot be repeated in the same row, column, or 3x3 subgrid.")
    print("5. Enter your move in the format: ColumnRow Number (e.g., 'G5 3').")
    print("\nTip: Use logic and elimination to find the correct numbers!")
    print("\nFor more details, visit: https://sudoku.com/easy/\n")

def load_game(choice):
    '''
    Loads the Sudoku board from a file based on the chosen difficulty.
    Each difficulty has its own pre-set puzzle saved as a JSON file.
    '''
    try:
        # Try to open and read the JSON file containing the board layout
        with open(f"sudoku/{choice}.json", 'r') as file:
            data = json.load(file)  # Parse the JSON data
        return data['board']  # Return the board from the file
    except FileNotFoundError:
        # If the file doesn't exist, print an error message
        print(f"Error: {choice}.json not found.")
        return None  # Return None to indicate the game couldn't be loaded

def save_game(choice, board):
    '''
    Saves the current Sudoku game state (the board) to a file.
    This happens when the player quits the game, so their progress is not lost.
    '''
  
    data = {'board': board}  # Structure data correctly

    try:
        with open(f"sudoku/{choice}", 'w') as file:  # Open the correct file
            json.dump(data, file, indent=4)  # Save as JSON with proper formatting
        print("Game saved successfully!")  
    except IOError:
        print("Error saving the game. Please try again.")

def display_board(board):
    '''
    Displays the current Sudoku board in a readable format.
    The board is a 9x9 grid with rows and columns, and visual separators between sections.
    '''
    print("\n   A B C  D E F   G H I")  # Column labels for reference (A to I)

    # Loop through each row in the board (there are 9 rows)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   -----+-----+-----")  # Add a separator every 3 rows for clarity
        
        row = [str(i + 1)]  # Label each row with its number (1 to 9)
        
        # Loop through each column in the current row (there are 9 columns)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row.append("|")  # Add a separator between every 3 columns
            
            # Show the value in the cell, replace 0 with a space (empty cell)
            row.append(str(board[i][j]) if board[i][j] != 0 else " ")  
        
        # Print the current row as a string with spaces between cells
        print(" ".join(row))
    print()  # Add a blank line at the end for neatness


def is_valid_move(board, move):
    '''
    This will return messages and true or false based on the move entered by the user
    This is the function enturing moves are in correct format and follow game logic
    '''

    columns = "ABCDEFGHI"  # This maps column letters (A-I) to indices (0-8)

    # Now we need to make it to where order in the move doesnt matter,
    # Because I wanted it to be one entry to do a whole move we have to split the move
    tokens = move.split() # now the move is in a token - a cordinate and number entry

    #This will control the order of the cordinates (first chunk)
    if len(tokens) != 2: # first see that the move has two chunnks ONLY 
        print("Error: Enter move in the following format 'G5 3'")
    
    
    #now we will create variable to call based on the split

    raw_coordinate = tokens[0].strip().lower() #This makes the cordinate lower and splits it again
    value = tokens[1].strip() #This will get the number the user wants in the cordinate

    #Make sure the cordinate is 2 pieces of data to continue
    if len(raw_coordinate) != 2:
        print("Error: incorrect cordinate")

    # now we will see if it is in the order I want, otherwise it will be flipped
    if raw_coordinate[0].isdigit() and raw_coordinate[1].isalpha(): # This will see if its in number letter format, if it is we will flip
        coordinate = raw_coordinate[0] + raw_coordinate[1] #this is the flip
    else:
        coordinate = raw_coordinate #otherwise no flip need so the raw_cord becomes the cordinate
    
    #Now that everything is split properly we will start validating

    col = columns.index(coordinate[0].upper())  # Convert column letter to index
    row = int(coordinate[1]) - 1  # Convert row number (1-9) to index (0-8)
    num = int(value)  # Convert the value input to an integer (1-9)

    # Validate the number (it must be between 1 and 9)
    if num < 1 or num > 9:
        print("Invalid number. Please enter a number between 1 and 9.")


    # Ensure we're not overwriting a pre-filled number (cells with 0 are empty)
    if board[row][col] != 0:
        print("That position is already filled. Choose another.")
        return False
    
    # Check 3x3 block
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                print("Invalid move: Number already exists in the 3x3 block.")
                return False

    
def update_board(board, move, row, col, value):
    '''
    Takes the player's move and updates the board accordingly.
    The move should be in the format "ColumnRow Number", e.g., "G5 3".
    '''
    if is_valid_move(move):
        # If all checks pass, update the board with the new number
        board[row][col] = value  
        return True  # Indicate that the board was successfully updated
    else:
        None

def play_game(board, choice):
    '''
    This is the main game loop where the user interacts with the Sudoku board.
    It runs until the user decides to quit or the game ends.
    '''
    while True:  # Keep looping until the user chooses to quit
        display_board(board)  # Show the current state of the board
        move = input("Enter your move or type 'quit' to exit: ").strip()  # Get the player's input
        os.system('cls')  # Clear the screen

        if move.lower() == "quit":
            print("Saving game...")
            save_game(choice, board)  # Save the game before quitting
            print("Thanks for playing!")
            return True  # Return True to signal that the game should fully exit

        elif update_board(board, move):
            os.system('cls')  # Clear the screen again after a valid move
            print("Move accepted!")  # Confirmation message
            time.sleep(1)  # Pause before clearing the screen
            os.system('cls')

        else:
            os.system('cls')
            print("Try again.")  # Inform the user that their move was invalid
            time.sleep(1)  # Give them a moment to read the message
            os.system('cls')

def main():
    '''
    Main function to manage the game setup, execution, and returning to the main menu.
    '''
    running = True  # Control the loop logically

    while running:
        choice = input("Enter a difficulty (Easy, Medium, Hard) or 'quit' to exit: ").capitalize()

        if choice.lower() == "quit":
            print("Exiting Sudoku. Goodbye!")
            running = False  # Stop the loop in the next iteration
        elif (board := load_game(choice)):  # Load the board and check if it's valid
            display_instructions()
            running = not play_game(board, choice)  # If play_game returns True, exit
        else:
            print("Invalid difficulty or file not found. Please try again.")



# Run the main function when the script is executed
if __name__ == "__main__":
    main()
