# 1. Name:
#      -your name-
# 2. Assignment Name:
#      Lab 01: Tic-Tac-Toe
# 3. Assignment Description:
#      Play the game of Tic-Tac-Toe
# 4. What was the hardest part? Be as specific as possible.
#      -a paragraph or two about how the assignment went for you-
# 5. How long did it take for you to complete the assignment?
#      -total time in hours including reading the assignment and submitting the program-

import json
import time
import keyboard

# The characters used in the Tic-Tac-Too board.
# These are constants and therefore should never have to change.
X = 'X'
O = 'O'
BLANK = ' '

# A blank Tic-Tac-Toe board. We should not need to change this board;
# it is only used to reset the board to blank. This should be the format
# of the code in the JSON file.
blank_board = {  
            "board": [
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK ]
        }

game_board = {'0': ' ' , '1': ' ' , '2': ' ' ,
            '3': ' ' , '4': ' ' , '5': ' ' ,
            '6': ' ' , '7': ' ' , '8': ' ' }

def read_board(filename):
    '''Read the previously existing board from the file if it exists.'''

    # request file name
    file_name = input("Enter the file name to open: ")

    # see if file name provided contains ".json" if not, add it to the end
    if not file_name.endswith(".json"):
        file_name += ".json"
    # Put file reading code here.

    #open the file path
    with open(file_name, 'r') as file:
        data = json.load(file)

    print("File found successfully!!")
     
    return blank_board['board']

def save_board(filename, board):

    if keyboard.read_key() == 'q':
        game_done = True
    '''Save the current game to a file.'''
    # Put file writing code here.
    with open('board.json', 'w') as f:
        json.dump(board, f)


def display_board(board):
    '''Display a Tic-Tac-Toe board on the screen in a user-friendly way.'''
    # Put display code here.

    print(board[0] + '|'+  board[1] + '|' + board[2])
    print("---+---+---")
    print(board[3] + '|'+  board[4] + '|' + board[5])
    print("---+---+---")
    print(board[6] + '|'+  board[7] + '|' + board[8])
    return


def is_x_turn(board):
    '''Determine whose turn it is.'''
    # Put code here determining if it is X's turn.


    #set the counter to 0
    square_count = 0

    # check for filled squares and add to count
    for square in board:
        if square != BLANK:
            square_count += 1
    
    # use mod to see if its X or O's turn
    if square_count % 2 == 0:
        return "X"
        
    else:
        return "O"
        
def play_game(board):
    '''Play the game of Tic-Tac-Toe.'''
    # Put game play code here. Return False when the user has indicated they are done.
    
    game_done = False

    while game_done != True:

        read_board(board)

        display_board(board)



def game_done(board, message=False):
    '''Determine if the game is finished.
       Note that this function is provided as-is.
       You do not need to edit it in any way.
       If message == True, then we display a message to the user.
       Otherwise, no message is displayed. '''

    # Game is finished if someone has completed a row.
    for row in range(3):
        if board[row * 3] != BLANK and board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if message:
                print("The game was won by", board[row * 3])
            return True

    # Game is finished if someone has completed a column.
    for col in range(3):
        if board[col] != BLANK and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
            return True

    # Game is finished if someone has a diagonal.
    if board[4] != BLANK and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
        return True

    # Game is finished if all the squares are filled.
    tie = True
    for square in board:
        if square == BLANK:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
        return True


    return False

# These user-instructions are provided and do not need to be changed.
print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
print("where the following numbers correspond to the locations on the grid:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 \n")
print("The current board is:")




# The file read code, game loop code, and file close code goes here.
