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

def update_board(board, move):
    '''
    Takes the player's move and updates the board accordingly.
    The move should be in the format "ColumnRow Number", e.g., "G5 3".
    '''
    columns = "ABCDEFGHI"  # This maps column letters (A-I) to indices (0-8)

    try:
        # Split the move into position (e.g., "G5") and number (e.g., "3")
        position, value = move.split()  
        col = columns.index(position[0].upper())  # Convert column letter to index
        row = int(position[1]) - 1  # Convert row number (1-9) to index (0-8)
        num = int(value)  # Convert the value input to an integer (1-9)

        # Validate the number (it must be between 1 and 9)
        if num < 1 or num > 9:
            print("Invalid number. Please enter a number between 1 and 9.")
            return False

        # Ensure we're not overwriting a pre-filled number (cells with 0 are empty)
        if board[row][col] != 0:
            print("That position is already filled. Choose another.")
            return False

        # If all checks pass, update the board with the new number
        board[row][col] = num  
        return True  # Indicate that the board was successfully updated

    except (IndexError, ValueError):
        # Handle invalid input (e.g., wrong format or out-of-bounds positions)
        print("Invalid input. Use format: ColumnRow Number (e.g., 'G5 3').")
        return False

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
    while True:  # Keep looping until the player chooses to quit
        choice = input("Enter a difficulty (Easy, Medium, Hard) or 'quit' to exit: ").capitalize()

        if choice.lower() == "quit":
            print("Exiting Sudoku. Goodbye!")
            break  # Exit the loop completely

        board = load_game(choice)
        if board:
            display_instructions()
            if play_game(board, choice):  # If play_game returns True, exit main()
                break
        else:
            print("Invalid difficulty or file not found. Please try again.")


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
