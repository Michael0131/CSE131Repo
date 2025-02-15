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

def is_valid_move(board, row, col, num):
    """
    Validates the user's move.
    Ensures proper input format and checks if the move is valid according to Sudoku rules.
    """
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


def update_board(board, coordinate, value):
    """
    Updates the board with the player's move if it's valid.
    """
    columns = "ABCDEFGHI"  # Maps column letters (A-I) to indices (0-8)
    
    # Normalize input to lowercase
    coordinate = coordinate.strip().lower()

    # Handle both formats (row-column or column-row)
    if coordinate[0].isdigit() and coordinate[1].isalpha():
        coordinate = coordinate[1] + coordinate[0]  # If format is '5G', flip it to 'G5'

    # Ensure the coordinate is valid
    if len(coordinate) != 2 or coordinate[0] not in columns or not coordinate[1].isdigit():
        print("Error: Invalid coordinate. Please enter a valid column (A-I) and row (1-9).")
        return False

    # Extract row and column from coordinate
    col = columns.find(coordinate[0].upper())  # Get column index
    row = int(coordinate[1]) - 1  # Convert row number (1-9) to index (0-8)

    # Validate the value
    if not value.isdigit() or not (1 <= int(value) <= 9):
        print("Error: Invalid number. Please enter a number between 1 and 9.")
        return False

    num = int(value)  # Convert the value to an integer

    # Check if the move is valid according to Sudoku rules
    if is_valid_move(board, row, col, num):
        board[row][col] = num  # Update the board with the valid move
        return True
    else:
        return False  # If the move is invalid, return False


def play_game(board):
    """
    Main game loop to interact with the Sudoku board. Continues until the player decides to quit.
    """
    while True:
        display_board(board)  # Show the current state of the board
        
        # Ask for the coordinate
        coordinate = input("Enter the coordinate (e.g., A1, B2, etc.) or 'quit' to exit: ").strip()

        if coordinate.lower() == 'quit':
            print("Saving game...")
            # save_game(board)  # Save the game before quitting (disabled in this example)
            print("Thanks for playing!")
            return True  # Return True to signal that the game should fully exit

        # Ensure the coordinate is valid
        if len(coordinate) < 2:
            print("Error: Invalid coordinate format. Try again.")
            continue

        # Ask for the value to be placed in the coordinate
        value = input(f"Enter the value to place at {coordinate}: ").strip()

        # Update the board with the move
        if update_board(board, coordinate, value):
            os.system('cls')  # Clear the screen after a valid move
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
        # Initial empty board for testing
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        print("Welcome to Sudoku!")
        
        # Call the game loop
        running = not play_game(board)  # If play_game returns True, exit

# Run the main function when the script is executed
if __name__ == "__main__":
    main()