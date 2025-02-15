# 1. Name:
#      Michael Johnson
# 2. Assignment Name:
#      Lab 06 : Sudoku Program
# 3. Assignment Description:
#      This program allows a user to play the game 'Sudoku' giving them a board and guidance to play the game.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part of testing is_valid_move() was ensuring that the function correctly identified conflicts in the row, column, 
# and 3x3 grid while handling different edge cases, such as incorrect input formats and out-of-range values. Debugging was challenging 
# because even when numbers weren’t visibly displayed due to a saving/loading issue, the program still recognized them as present, making 
# validation trickier. Ensuring the test cases covered enough scenarios without being excessive required balancing thoroughness with simplicity.
# 5. How long did it take for you to complete the assignment?
#      3 1/2 hours



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

def load_game(difficulty):
    '''
    Loads the Sudoku board from a file based on the chosen difficulty.
    Each difficulty has its own pre-set puzzle saved as a JSON file.
    
    Parameters:
        difficulty (str): The difficulty level chosen by the user.
        
    Returns:
        list: The 9x9 Sudoku board if file is found, else None.
    '''
    try:
        with open(f"sudoku/{difficulty}.json", 'r') as file:
            data = json.load(file)  # Parse the JSON data
        return data['board']  # Return the board from the file
    except FileNotFoundError:
        print(f"Error: {difficulty}.json not found.")
        return None  # Indicate the game couldn't be loaded

def save_game(difficulty, board):
    '''
    Saves the current Sudoku game state (the board) to a file.
    This happens when the player quits the game, so their progress is not lost.
    
    Parameters:
        difficulty (str): The difficulty level used to name the file.
        board (list): The current 9x9 Sudoku board.
    '''
    file_name = f"sudoku/{difficulty}.json"  # Ensure consistency with load_game()
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
    Converts each cell to an integer before checking if it is zero.
    If a cell’s integer value is zero, a blank space is printed;
    otherwise, the number is shown.
    
    Parameters:
        board (list): The current 9x9 Sudoku board.
    '''
    # Print column headers
    print("\n   A B C  D E F   G H I")
    
    # Iterate over each row (0 to 8)
    for row_index in range(9):
        # Print a horizontal separator after every 3 rows (except the first)
        if row_index % 3 == 0 and row_index != 0:
            print("   -----+-----+-----")
        
        # Start building the display string for the row with the row number (1-indexed)
        row_display = [str(row_index + 1)]
        
        # Iterate over each column (0 to 8)
        for col_index in range(9):
            # Add a vertical separator after every 3 columns (except the first)
            if col_index % 3 == 0 and col_index != 0:
                row_display.append("|")
            # Convert the cell value to an integer before comparison.
            cell_value = board[row_index][col_index]
            try:
                numeric_value = int(cell_value)
            except (ValueError, TypeError):
                numeric_value = 0  # Default to 0 if conversion fails
            
            # Append the number if nonzero; otherwise, append a blank space
            if numeric_value != 0:
                row_display.append(str(numeric_value))
            else:
                row_display.append(" ")
        
        # Print the assembled row
        print(" ".join(row_display))
    print()  # Add a final blank line for neatness

def format_cord(coordinate):
    '''
    Formats the coordinate so it is consistent throughout the program.
    Converts the input to uppercase and, if in "DigitLetter" format (e.g., "1A"),
    swaps the order to "A1".
    
    Parameters:
        coordinate (str): The coordinate input by the user.
        
    Returns:
        str: The formatted coordinate.
    '''
    coordinate = coordinate.strip().upper()
    # If coordinate is in 'DigitLetter' format, swap to 'LetterDigit'
    if len(coordinate) >= 2 and coordinate[0].isdigit() and coordinate[1].isalpha():
        coordinate = coordinate[1] + coordinate[0]  # Swap "1A" -> "A1"
    return coordinate

def is_valid_move(board, coordinate, value):
    """
    Validates the user's move.
    Checks the coordinate format, ensures the cell is empty,
    and confirms that placing the value adheres to Sudoku rules.
    
    Parameters:
        board (list): The current 9x9 Sudoku board.
        coordinate (str): The coordinate where the move is to be made.
        value (str): The value to be placed at the coordinate.
        
    Returns:
        bool: True if the move is valid, False otherwise.
    """
    coordinate = format_cord(coordinate)
    # Ensure the coordinate is in the format of a letter (A-I) and a digit (1-9)
    if len(coordinate) != 2 or not (coordinate[0].isalpha() and coordinate[1].isdigit()):
        print("Invalid input: Coordinate format is incorrect.")
        return False

    # Convert coordinate to board indices
    row_index = int(coordinate[1]) - 1
    col_index = ord(coordinate[0]) - ord('A')
    
    # Check if the provided value is a digit between 1 and 9
    if not value.isdigit() or not (1 <= int(value) <= 9):
        print("Invalid number: Must be between 1 and 9.")
        return False
    
    numeric_value = int(value)
    
    # Check if the cell is already occupied
    if board[row_index][col_index] != 0:
        print("That position is already filled. Choose another.")
        return False

    # Check for duplicate in the row
    if numeric_value in board[row_index]:
        print("Invalid move: Number already exists in the row.")
        return False

    # Check for duplicate in the column
    for current_row in range(9):
        if board[current_row][col_index] == numeric_value:
            print("Invalid move: Number already exists in the column.")
            return False

    # Determine the 3x3 block and check for duplicates within it
    block_row_start = (row_index // 3) * 3
    block_col_start = (col_index // 3) * 3
    for block_row in range(block_row_start, block_row_start + 3):
        for block_col in range(block_col_start, block_col_start + 3):
            if board[block_row][block_col] == numeric_value:
                print("Invalid move: Number already exists in the 3x3 block.")
                return False

    return True  # Move passes all checks

def update_board(board, coordinate, value):
    '''
    Updates the board with the player's move if the move is valid.
    
    Parameters:
        board (list): The current 9x9 Sudoku board.
        coordinate (str): The coordinate where the move is to be made.
        value (str): The value to be placed at the coordinate.
        
    Returns:
        bool: True if the board was updated (move is valid), False otherwise.
    '''
    if is_valid_move(board, coordinate, value):
        formatted_coord = format_cord(coordinate)
        row_index = int(formatted_coord[1]) - 1
        col_index = ord(formatted_coord[0]) - ord('A')
        board[row_index][col_index] = int(value)  # Update the board cell with the numeric value
        return True
    else:
        return False

def play_game(board, difficulty):
    '''
    Main game loop where the user interacts with the Sudoku board.
    Continues until the user decides to quit.
    
    Parameters:
        board (list): The current 9x9 Sudoku board.
        difficulty (str): The current game difficulty used for saving.
        
    Returns:
        bool: True if the game was ended by quitting.
    '''
    game_running = True  # Flag to control the game loop

    while game_running:
        display_board(board)  # Display the current board state
        user_input = input("Enter coordinate 'Example: G5' or 'Q' to quit: ").strip()
        
        # Check if the user wants to quit immediately
        if user_input.upper() == 'Q':
            save_game(difficulty, board)  # Save game state
            print("Exiting Sudoku. Goodbye!")
            game_running = False  # End the game loop
        else:
            # Format and validate the coordinate input
            formatted_coord = format_cord(user_input)
            is_coord_valid = (len(formatted_coord) == 2 and 
                              formatted_coord[0].isalpha() and 
                              formatted_coord[1].isdigit())
            
            if is_coord_valid:
                # Get the value to be placed at the coordinate
                cell_value = input("Enter value 'Example 6': ").strip()
                os.system('cls')  # Clear the screen for a fresh display
                if update_board(board, formatted_coord, cell_value):
                    os.system('cls')  # Clear screen after a successful move
                    print("Move accepted!")
                    time.sleep(2)  # Pause for user to see confirmation
                    os.system('cls')
                else:
                    print("Try again.")
                    time.sleep(2)
                    os.system('cls')
            else:
                # If the coordinate format is invalid, display an error message
                print("Error: Invalid Coordinate.")
                time.sleep(2)
                os.system('cls')
    # Game loop ended because the user quit
    return True  # Indicate that the game was ended by quitting

def test_is_valid_move():
    """
    Minimal tests for the is_valid_move() function.
    Each test is a tuple of (description, board, coordinate, value, expected_result).
    """
    print("Running minimal test cases for is_valid_move()...\n")
    
    # Create an empty 9x9 board (all zeros)
    empty_board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Test cases:
    tests = [
        # 1. Valid move on an empty board.
        ("Valid move on empty board", empty_board, "A1", "5", True),
        # 2. Invalid coordinate format.
        ("Invalid coordinate format", empty_board, "11", "5", False),
        # 3. Invalid value (out of range).
        ("Invalid value (out of range)", empty_board, "A1", "10", False),
        # 4. Duplicate in row.
        ("Duplicate in row", 
         # Create a board with a 5 in the first cell of row 1.
         [[5] + [0]*8] + [[0]*9 for _ in range(8)],
         "B1", "5", False)
    ]
    
    passed = 0
    failed = 0
    
    for desc, board, coord, val, expected in tests:
        result = is_valid_move(board, coord, val)
        if result == expected:
            print(f"PASS: {desc} (Input: {coord} {val})")
            passed += 1
        else:
            print(f"FAIL: {desc} (Input: {coord} {val}). Expected {expected}, got {result}")
            failed += 1
            
    print(f"\nTest Summary: {passed} passed, {failed} failed.\n")


def main():
    '''
    Main function to manage game setup, execution, and returning to the main menu.
    '''
    app_running = True  # Flag to control the main application loop

    while app_running:
        # Ask the user for a difficulty level
        difficulty = input("Enter a difficulty (Easy, Medium, Hard): ").capitalize()
        
        # Attempt to load a game board for the given difficulty
        if (board := load_game(difficulty)):
            display_instructions()
            # If the user quits during play_game, exit the main loop
            app_running = not play_game(board, difficulty)
        else:
            print("Invalid difficulty or file not found. Please try again.")

# Run the main function when the script is executed
if __name__ == "__main__":
    test_is_valid_move()
    main()
