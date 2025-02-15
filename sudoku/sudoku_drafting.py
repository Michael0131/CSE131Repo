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
        with open(f"sudoku/{choice}.json", 'r') as file:
            data = json.load(file)  # Parse the JSON data
        return data['board']  # Return the board from the file
    except FileNotFoundError:
        print(f"Error: {choice}.json not found.")
        return None  # Return None to indicate the game couldn't be loaded

def save_game(choice, board):
    '''
    Saves the current Sudoku game state (the board) to a file.
    This happens when the player quits the game, so their progress is not lost.
    '''
    file_name = f"sudoku/{choice}.json"  # Ensure consistency with load_game()

    data = {'board': board}  # Structure data correctly

    try:
        with open(file_name, 'w') as file:  # Open the correct file
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

def format_cord(coordinate):
    '''
    This is going to format the coordinate so it is the same throughout the program.
    It converts the input to uppercase and, if in "DigitLetter" format (e.g., "1A"),
    it swaps the order to "A1".
    '''
    coordinate = coordinate.strip().upper()

    # Check if the input is in the 'DigitLetter' format (e.g., '1A') and swap if needed
    if len(coordinate) >= 2 and coordinate[0].isdigit() and coordinate[1].isalpha():
        coordinate = coordinate[1] + coordinate[0]  # Swap "1A" -> "A1"
    
    return coordinate

def is_valid_move(board, coordinate, value):
    """
    Validates the user's move.
    Ensures proper input format and checks if the move is valid according to Sudoku rules.
    """
    coordinate = format_cord(coordinate)

    # Ensure coordinate is in the format of a letter (A-I) and a digit (1-9)
    if len(coordinate) != 2 or not (coordinate[0].isalpha() and coordinate[1].isdigit()):
        print("Invalid input: Coordinate format is incorrect.")
        return False

    # Extract row and column from coordinate
    row, col = int(coordinate[1]) - 1, ord(coordinate[0]) - ord('A')

    # Check if the value is valid (should be between 1 and 9)
    if not value.isdigit() or not (1 <= int(value) <= 9):
        print("Invalid number: Must be between 1 and 9.")
        return False

    value = int(value)

    # Check if the position is already filled
    if board[row][col] != 0:
        print("That position is already filled. Choose another.")
        return False

    # Check for uniqueness in the row
    if value in board[row]:
        print("Invalid move: Number already exists in the row.")
        return False

    # Check for uniqueness in the column
    for i in range(9):
        if board[i][col] == value:
            print("Invalid move: Number already exists in the column.")
            return False

    # Check 3x3 subgrid for conflicts
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == value:
                print("Invalid move: Number already exists in the 3x3 block.")
                return False

    return True  # If all checks pass, the move is valid

def update_board(board, coordinate, value):
    '''
    Takes the player's move and updates the board accordingly.
    The move should be in the format "ColumnRow Number", e.g., "G5 3".
    '''
    # Call the is_valid_move function to check if the move is valid
    if is_valid_move(board, coordinate, value):
        row, col = int(format_cord(coordinate)[1]) - 1, ord(format_cord(coordinate)[0]) - ord('A')
        board[row][col] = int(value)  # Update the board with the valid move
        return True
    else:
        return False  # If the move is invalid, return False

def play_game(board, choice):
    '''
    This is the main game loop where the user interacts with the Sudoku board.
    It runs until the user decides to quit or the game ends.
    (No use of continue, break, or exit.)
    '''
    run_game = True  # Flag to control the loop
    while run_game:
        display_board(board)  # Show the current state of the board
        coordinate = input("Enter coordinate 'Example: G5' or 'Q' to quit: ").strip()
        
        # First, check if the user wants to quit.
        if coordinate.upper() == 'Q':
            save_game(choice, board)  # Save the game before quitting
            print("Exiting Sudoku. Goodbye!")
            run_game = False
        else:
            # Format and validate the coordinate
            coordinate = format_cord(coordinate)
            valid_coordinate = (len(coordinate) == 2 and coordinate[0].isalpha() and coordinate[1].isdigit())
            if valid_coordinate:
                value = input("Enter value 'Example 6': ").strip()  # Get the player's value input
                os.system('cls')  # Clear the screen
                if update_board(board, coordinate, value):
                    os.system('cls')  # Clear the screen again after a valid move
                    print("Move accepted!")  # Confirmation message
                    time.sleep(2)  # Pause before clearing the screen
                    os.system('cls')
                else:
                    print("Try again.")
                    time.sleep(2)
                    os.system('cls')
            else:
                print("Error: Invalid Coordinate.")
                time.sleep(2)
                os.system('cls')
    # When run_game becomes False, the loop ends naturally
    return True  # Indicate that the game was ended (quit)

def main():
    '''
    Main function to manage the game setup, execution, and returning to the main menu.
    '''
    running = True  # Control the loop logically

    while running:
        choice = input("Enter a difficulty (Easy, Medium, Hard): ").capitalize()

        if (board := load_game(choice)):  # Load the board and check if it's valid
            display_instructions()
            # If play_game returns True (user quit), then set running to False to exit main.
            running = not play_game(board, choice)
        else:
            print("Invalid difficulty or file not found. Please try again.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
