"""
This module implements the famous Connect 4 game. It should allow the game to be played either by two
humans, a human against a computer, or by the computer against itself. The module should also
allow the current game to be saved, and a previously saved game to be loaded and continued.  
Thang Phan 10336709
"""

from copy import deepcopy # you may use this for copying a board
from sys import exit
from random import choice

def newGame(player1,player2):
    """
    The function returns a game dictionary. 
    In this dictionary all the positions of the board are empty (i.e., all are set to the integer 0),
    the players' names are set to the input parameters of the function, and the variable who is
    set to the integer 1 (in a new game, player 1 will always make the first move).
    """
    
    game = {'player1' : player1,
            'player2' : player2,
            'who' : 1,
            'board' : [[0] * 7 for i in range(6)]
            }
    return game

def printBoard(board):
    """
    The function takes as input a list board representing the Connect Four board and
    prints the 7x6 Connect Four board in a nicely formatted fashion.
    """
    board1 = deepcopy(board)
    for y in range(6):
        for x in range(7):
            if board1[y][x] == 1:
                board1[y][x] = "X"
            if board1[y][x] == 2:
                board1[y][x] = "O"
            if board1[y][x] == 0:
                board1[y][x] = " "
                
    print()
    print(' ', end='')
    for x in range(1,8):
        print(' %s  ' % x, end='')
    print()
    print('+' + ('---+' * 7))
    for y in range(6):
        print('|', end='')
        for x in range(7):
            print(' %s |' % board1[y][x], end='')
        print()
        print('+' + ('---+' * 7))
    print()

def getValidMoves(board):
    """
    The function takes the board from the game dictionary and
    returns a list of integers between 0,1,...,6 corresponding to the indices of the board
    columns which are not completely filled by checking the first row on the board.
    """
    valid = []
    for i in range(7):
        if board[0][i] == 0:
            valid.append(i)
    return valid

def makeMove(board,move,who):
    """
    The function takes as input a list board representing the Connect Four board, an integer move
    between 0,1,...,6, and an integer who with possible values 1 or 2. The parameter move corresponds to
    the column index into which the player with number who will insert their "disc". The function then
    returns the updated board variable. 
    """
    for y in range (5,-1,-1):
        if board[y][move] == 0:
            board[y][move] = who
            return board
    
def hasWon(board,who):
    """
    The function takes as input a list board representing the Connect Four board and an integer who with
    possible values 1 or 2. The function returns True or False. It returns True if the player with number
    who occupies four adjacent positions which form a horizontal, vertical, or diagonal line. The function
    returns False otherwise.
    """
    # Check rows
    for x in range(4):
        for y in range(6):
            if (board[y][x] == who and board[y][x+1] == who and board[y][x+2] == who and board[y][x+3] == who):
                return True

    # Check columns 
    for x in range(7):
        for y in range(3):
            if (board[y][x] == who and board[y+1][x] == who and board[y+2][x] == who and board[y+3][x] == who):
                return True

    # Check negative diagonal
    for x in range(4):
        for y in range(3):
            if (board[y][x] == who and board[y+1][x+1] == who and board[y+2][x+2] == who and board[y+3][x+3] == who):
                return True

    # Check postive diagonal
    for x in range(4):
        for y in range(3,6):
            if (board[y][x] == who and board[y-1][x+1] == who and board[y-2][x+2] == who and board[y-3][x+3] == who):
                return True

    return False

def suggestMove1(board,who):
    """
    The function takes as input a list board representing the Connect Four board, an integer who that's either 1 or 2
    The function returns an integer between 0,1,...,6 corresponding to a column index of the board
    into which player number who should insert their "disc". This column index is determined as follows:
    
    -First check if among all valid moves of player number who there is a move which leads to an
    immediate win of this player. In this case, return such a winning move.
    
    -If there is no winning move for player number who, we will try to prevent the other player from
    winning. This is done by checking if there is a winning move for the other player and returning it.
    
    -Otherwise, if there is no immediate winning move for both players, the function simply returns a
    valid move which will be the first valid move. 
    """
    board2 = deepcopy(board)
    #Check if the player who can win now
    
    for move in getValidMoves(board):
        makeMove(board2,move,who)
        if hasWon(board2,who):
            return move
        else:
            board2 = deepcopy(board)
    #Block if the oppnent can win
    
    if who == 1:
        for move in getValidMoves(board):
            makeMove(board2,move,who+1)
            if hasWon(board2,who+1):
                return move
            else:
                board2 = deepcopy(board)
        
    if who == 2:
        for move in getValidMoves(board):
            makeMove(board2,move,who-1)
            if hasWon(board2,who-1):
                return move
            else:
                board2 = deepcopy(board)
    
    #1st Choice
    return getValidMoves(board)[0]

def suggestMove2(board,who):
    """
    The function takes as input a list board representing the Connect Four board, an integer who that's either 1 or 2
    The function returns an integer between 0,1,...,6 corresponding to a column index of the board
    into which player number who should insert their "disc". This column index is determined as follows:
    
    -First check if among all valid moves of player number who there is a move which leads to an
    immediate win of this player. In this case, return such a winning move.
    
    -If there is no winning move for player number who, we will try to prevent the other player from
    winning. This is done by checking if there is a winning move for the other player and returning it.
    
    -If there is no immediate winning move for both players, the function returns a
    move if either player can win within 2 moves.
    
    -Else, it will return a few set moves initally, then return a random valid move.
    """
    board2 = deepcopy(board)
    #Check if the computer who can win now
    
    for move in getValidMoves(board):
        makeMove(board2,move,who)
        if hasWon(board2,who):
            return move
        else:
            board2 = deepcopy(board)
    #Block if the oppnent can win
    
    if who == 1:
        for move in getValidMoves(board):
            makeMove(board2,move,who+1)
            if hasWon(board2,who+1):
                return move
            else:
                board2 = deepcopy(board)
        
    if who == 2:
        for move in getValidMoves(board):
            makeMove(board2,move,who-1)
            if hasWon(board2,who-1):
                return move
            else:
                board2 = deepcopy(board)
                
#First few moves will be in the played to reduce the chances of an easy win
    if board[5][3] == 0 and who == 1:
        return 3
    if board[5][4] == 0 and who == 1:
        return 4
    if board[5][2] == 0 and who == 2:
        return 2
    
    #Block if the opponent can win in two moves
    if who == 1:
        for firstmove in getValidMoves(board):
            makeMove(board2,firstmove,who+1)
            board3 = deepcopy(board2)
            for secondmove in getValidMoves(board):
                makeMove(board3,secondmove,who+1)
                if hasWon(board3,who+1):
                    if secondmove == firstmove:
                        try:
                            playmove = deepcopy(getValidMoves(board))
                            playmove.remove(secondmove)
                            return choice(playmove)
                        except ValueError:
                            return choice(getValidMoves(board))
                    else:
                        return secondmove
                else:
                    board3 = deepcopy(board2)
            board2 = deepcopy(board)
            
    #if who == 2:
        for firstmove in getValidMoves(board):
            makeMove(board2,firstmove,who-1)
            board3 = deepcopy(board2)
            for secondmove in getValidMoves(board):
                makeMove(board3,secondmove,who-1)
                if hasWon(board3,who-1):
                    if secondmove == firstmove:
                        try:
                            playmove = deepcopy(getValidMoves(board))
                            playmove.remove(secondmove)
                            return choice(playmove)
                        except ValueError:
                            return choice(getValidMoves(board))
                    else:
                        return secondmove
                else:
                    board3 = deepcopy(board2)
            board2 = deepcopy(board)

    #If computer can win in two moves
    for firstmove in getValidMoves(board):
        makeMove(board2,firstmove,who)
        board3 = deepcopy(board2)
        for secondmove in getValidMoves(board):
            makeMove(board3,secondmove,who)
            if hasWon(board3,who):
                return secondmove
            else:
                board3 = deepcopy(board2)
        board2 = deepcopy(board)

    #Random Choice
    return choice(getValidMoves(board))

def loadGame(filename):
    """
    The function attempts to open a text file with the input, filename, and returns its contents
    in form of a game dictionary.
    """
    if filename == '':
        filename = 'game.txt'  #If filename isn't given, the file game.txt is assumed
    if not filename.endswith('.txt'):
        filename = filename + '.txt'
    game,var,board = {},[],[]
    with open(filename) as f:
        for line in f:
            line = line[0:len(line)].replace("\n","")
            var.append(line)
    game['player1'],game['player2'],game['who'] = var[0],var[1],int(var[2])
    if game['who'] == 1 or game['who'] == 2:    #Check if the format of who is correct
        for i in range(6):    
            g = [int(s) for s in var[i+3].split(',') if s == '0' or s == '1' or s == '2']
            if len(g) == 7:     #Check if the format of the board is correct
                board.append(g)
            else:
                raise ValueError
        game['board'] = board
    else:
        raise ValueError
    return game

def saveGame(game,filename):
    """
    The function takes the game dictionary and a string variable called filename and
    the function writes the game state into a text file with the name as the input filename
    in the specified format and return to the play function
    """
    game1 = deepcopy(game)
    if filename == '':
        filename = 'game.txt'  #If filename isn't given, the file game.txt is assumed
    if not filename.endswith('.txt'):
        filename = filename + '.txt'
    try:    
        with open(filename, mode="wt", encoding="utf8") as f:
            for key,val in game1.items():
                if key == "board":
                    for i in range(len(val)):
                        val[i] = ','.join(i for i in str(val[i]).replace(", ",",").split(','))[1:-1]
                        f.write(val[i] + "\n")
                else:
                    f.write(str(val)+"\n")
    except IOError:
        print("Unable to save")
        return

# ------------------- Main function --------------------
def play():
    """ 
    This function will take care of the overall operation of the game.
    Start of the Connect 4 Game when play() is called (Welcomes the player/s):
    -It will ask for each player's name. If either name is "C" then the player is controlled by the computer.
    -If either name is "L" then a previous game can be continued. 
    -Then the game of Connect 4 will start with either a loaded or a new game.
    -Each player/computer will make a move until someone wins or the board is full.
    """
    print("*"*54)
    print("***"+" "*8+"WELCOME TO THANG'S CONNECT FOUR!"+" "*8+"***")
    print("*"*54,"\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
#Setup    
    player1 = input("1st Player's name: ").capitalize()
    if player1 == 'L':
        try:
            filename = input('What is the filename? (Make sure to include .txt) : ')
            game = loadGame(filename)
        except FileNotFoundError:
            print('The file has not been found.')
            exit(1)
        except ValueError or IndexError:
            print('An error occured trying to read the file')
            exit(1)
    else:
        player2 = input("2nd Player's name: ").capitalize()
        if player2 == 'L':
            try:
                filename = input('What is the filename? (Make sure to include .txt) : ')
                game = loadGame(filename)
            except IOError:
                print('An error occurred trying to read the file.')
        else:
            game = newGame(player1,player2)
    
    board, who, player1, player2 = game['board'], game["who"], game['player1'], game['player2']
    printBoard(board)
#Game    
    while len(getValidMoves(board)) > 0:
        if who == 1:
            if player1 != 'C':
                try:
                    move = input("{} (X): Choose a column or type 'S' to save or type 'Q' to quit: ".format(player1))
                    move = int(move)-1
                    if move in getValidMoves(board):
                        makeMove(board,move,who)
                        printBoard(board)
                        if hasWon(board,who):
                            print("{}, You won! Congratulations!".format(player1))
                            exit(1)
                        who = 2
                    else:
                        if move <= 7 and move >= 1:
                            print("Sorry, invalid square. Please try again!")
                        else:
                            raise ValueError
                except ValueError:
                    if str(move).capitalize() == 'S':
                        game['who'] = who
                        filename = input("What would you like the file name to be? : ")
                        saveGame(game,filename)
                        continue
                    if str(move).capitalize() == 'Q':
                        exit(1)
                    else:
                        print('Only numbers between 1 and 7, "S" to save or "Q" to quit, are allowed')
                        continue
            else:
                move = suggestMove2(board,who)
                print("Computer (X) has selected column {}.".format(move))
                makeMove(board,move,who)
                printBoard(board)
                if hasWon(board,who):
                    print("The Computer (X) has won!")
                    exit(1)
                who = 2
#Player 2                    
        else:
            if player2 != 'C':
                try:
                    move = input("{} (O): Choose a column, type 'S' to save or type 'Q' to quit: ".format(player2))
                    move = int(move)-1
                    if move in getValidMoves(board):
                        makeMove(board,move,who)
                        printBoard(board)
                        if hasWon(board,who):
                            print("{}, You won! Congratulations!".format(player2))
                            exit(1)
                        who = 1
                    else:
                        if move <= 7 and move >= 1:
                            print("Sorry, invalid square. Please try again!")
                        else:
                            raise ValueError
                except ValueError:
                    if str(move).capitalize() == 'S':
                        game['who'] = who
                        filename = input("What would you like the file name to be? : ")
                        saveGame(game,filename)
                        continue
                    if str(move).capitalize() == 'Q':
                        exit(1)
                    else:
                        print('Only numbers between 1 and 7, "S" to save or "Q" to quit, are allowed')
                        continue
            else:
                move = suggestMove2(board,who)
                print("Computer (O) has selected column {}.".format(move))
                makeMove(board,move,who)
                printBoard(board)
                if hasWon(board,who):
                    print("The Computer (O) has won!")
                    exit(1)
                who = 1
    print("It's a draw")
    exit(1)

# the following allows your module to be run as a program

if __name__ == '__main__' or __name__ == 'builtins':
    play()
