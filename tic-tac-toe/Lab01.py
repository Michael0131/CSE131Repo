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
import os

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

def read_board(filename):
    '''Read the previously existing board from the file if it exists.'''
    # Put file reading code here.

    # try and read from the file "tictactoe.json" 
    # if it cant find it just return a blank board

    try:
        with open("tic-tac-toe/tictactoe.json", 'r') as file:
            data = json.load(file)
        return data['board']
    except (FileNotFoundError):
        return blank_board['board']

def save_board(filename, board):
    '''Save the current game to a file.'''
    # Put file writing code here.

    # open the tictactoe.json file and write to it the board
    with open("tic-tac-toe/tictactoe.json", "w") as file:
        json.dump({'board': board}, file)

def display_board(board):
    '''Display a Tic-Tac-Toe board on the screen in a user-friendly way.'''
    # Put display code here.

    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def is_x_turn(board):
    '''Determine whose turn it is.'''
    # Put code here determining if it is X's turn.

    # get the count of x and 0, when they have the same number its x's turn
    # if o has less than it is o's turn, etc.
    x_count = board.count(X)
    o_count = board.count(O)
    if x_count == o_count:
        return True

def play_game(board):
    '''Play the game of Tic-Tac-Toe.'''
    # Put game play code here. Return False when the user has indicated they are done.

    while True:
        # start the game by displaying the board
        os.system('cls')
        display_instructions()
        display_board(board)

        # get what players turn it is
        # if is_x_turn is true than its X's turn, otherwise it is O's turn
        current_player = X if is_x_turn(board) else O

        #get the current players input
        print(f"{current_player}'s turn. Enter a number (1-9) or 'q' to quit:")
        # have user input in the required format
        move = input("> ")

         # convert player input to lower and if its 'q' close game
        if move.lower() == 'q':
            print("Please wait while we save your game :)")
            time.sleep(2)
            save_board(file_name, board)
            exit() # end/close the game
        
        # see if input is a number and within the bounds, if not show error, but allow re entry
        if not move.isdigit() or int(move) < 1 or int(move) > 9:
            os.system('cls')
            print("ERROR! Invalid Input: Chose a number from (1-9)")
            time.sleep(2)
            os.system('cls')
            continue

        # get the position, and format it for the index
        position = int(move) - 1

        #check if position is empty, if not alrt user and allow re entry
        if board[position] != BLANK:
            print("This space is full, chose another!")
            continue

        #set board position to current player
        board[position] = current_player

        if game_done(board, message = False):
            display_board(board)
            return False # end the game

    

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
                time.sleep(3)
            return True

    # Game is finished if someone has completed a column.
    for col in range(3):
        if board[col] != BLANK and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
                time.sleep(2)
            return True

    # Game is finished if someone has a diagonal.
    if board[4] != BLANK and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
            time.sleep(2)
        return True

    # Game is finished if all the squares are filled.
    tie = True
    for square in board:
        if square == BLANK:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
            time.sleep(2)
        return True


    return False

# These user-instructions are provided and do not need to be changed.

#make this a function to call easier
def display_instructions():
    print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
    print("where the following numbers correspond to the locations on the grid:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 \n")
    print("The current board is:")

# The file read code, game loop code, and file close code goes here.



# check tic tac toe file and load if available
file_name = "tictactoe.json"
board = read_board(file_name)

active_game = True

while active_game:

    #start playing the game
    active_game = play_game(board)

    # now that players can do moves must see if game is won
    # if it is, reset board, if player doesnt want to, they have the 'q' option
    if game_done(board, message = True):

        #once game is done let player know game is resetting
    
        print("Resetting Game. Please wait...")
        time.sleep(2)
        
        #reset the board
        board = blank_board['board']
        #write over the last game and save
        save_board(file_name, board)

        #notify user that game is ready
    
        print("The game has been reset. Start playing again!")
        time.sleep(2)
        

        #show the instructions again and the new board
        display_instructions()
        display_board(board)
        active_game = play_game(board)


        



