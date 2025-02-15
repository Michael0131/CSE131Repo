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
    if not os.path.exists(f"sudoku/{choice}.json"):
        print(f"Error: {choice}.json not found.")
        return None  # Return None to indicate the game couldn't be loaded
    with open(f"sudoku/{choice}.json", 'r') as file:
        data = json.load(file)  # Parse the JSON data
    return data['board']  # Return the board from the file

def save_game(choice, board):
    '''
    Saves the current Sudoku game state (the board) to a file.
    This happens when the player quits the game, so their progress is not lost.
    '''
    data = {'board': board}  # Structure data correctly
    with open(f"sudoku/{choice}.json", 'w') as file:  # Open the correct file
        json.dump(data, file, indent=4)  # Save as JSON with proper formatting
    print("Game saved successfully!")

def display_board(board):
    '''
    Displays the current Sudoku board in a readable format.
    The board is a 9x9 grid with rows and columns, and visual separators between sections.
    '''
    print("\n   A B C  D E F   G H I")  # Column labels for reference (A to I)

    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   -----+-----+-----")  # Add a separator every 3 rows for clarity
        
        row = [str(i + 1)]  # Label each row with its number (1 to 9)
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row.append("|")  # Add a separator between every 3 columns
            
            row.append(str(board[i][j]) if board[i][j] != 0 else " ")  # Show the value in the cell
        print(" ".join(row))
    print()

def is_valid_move(board, move):
    """
    Validates the user's move.
    Ensures proper input format and checks if the move is valid according to Sudoku rules.
    """
    columns = "ABCDEFGHI"  # Maps column letters (A-I) to indices (0-8)
    tokens = move.split()  # Split the move into coordinate and number

    if len(tokens) != 2:
        print("Error: Enter move in the following format 'G5 3'")
        return False

    raw_coordinate = tokens[0].strip().lower()  # Normalize input to lowercase
    value = tokens[1].strip()  # The number the user wants to enter

    if len(raw_coordinate) != 2:
        print("Error: Incorrect coordinate format.")
        return False

    # Handle both formats (row-column or column-row)
    if raw_coordinate[0].isdigit() and raw_coordinate[1].isalpha():
        coordinate = raw_coordinate[1] + raw_coordinate[0]  # If format is '5G', flip it to 'G5'
    else:
        coordinate = raw_coordinate  # If format is 'G5', keep it as it is

    if coordinate[0].upper() not in columns or not (1 <= int(coordinate[1]) <= 9):
        print("Error: Invalid coordinate. Please enter a valid column (A-I) and row (1-9).")
        return False

    col = columns.find(coordinate[0].upper())  # Convert column letter to index
    row = int(coordinate[1]) - 1  # Convert row number (1-9) to index (0-8)

    if not value.isdigit() or not (1 <= int(value) <= 9):
        print("Error: Invalid number. Please enter a number between 1 and 9.")
        return False

    num = int(value)

    # Check if the position is already filled
    if board[row][col] != 0:
        print("That position is already filled. Choose another.")
        return False

    # Check for uniqueness in the row
    if num in board[row]:
        print("Invalid move: Number already exists in the row.")
        return False

    # Check for uniqueness in the column
    for i in range(9):
        if board[i][col] == num:
            print("Invalid move: Number already exists in the column.")
            return False

    # Check 3x3 subgrid for conflicts
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                print("Invalid move: Number already exists in the 3x3 block.")
                return False

    return True  # If all checks pass, the move is valid


def update_board(board, move):
    """
    Updates the board with the player's move if it's valid.
    """
    tokens = move.split()
    raw_coordinate = tokens[0].strip().lower()  # Coordinate (e.g., 'g5')
    value = tokens[1].strip()  # The number the user wants to enter

    col = "ABCDEFGHI".find(raw_coordinate[0].upper())  # Get column index
    row = int(raw_coordinate[1]) - 1  # Get row index

    num = int(value)  # Convert the number to an integer
    if is_valid_move(board, move):
        board[row][col] = num  # Update the board
        return True  # Indicate that the board was successfully updated
    else:
        return False  # If invalid, return False


def play_game(board, choice):
    """
    Main game loop to interact with the Sudoku board. Continues until the player decides to quit.
    """
    while True:
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
    """
    Main function to manage the game setup, execution, and returning to the main menu.
    """
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
