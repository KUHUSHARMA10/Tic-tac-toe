"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    This creates a 3 by 3 board filled with EMPTY 
Think of it as your game start point. Its just a fresh board. Nothing fancy, but everything builds on this.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    The player function should take a board state as input, and return which players turn it is (either X or O).
    """
    Xcount = 0 # counts the number of x ensuring players alternate turns correctly
    Ocount = 0

    for row in board: # basically a 2d list
        Xcount += row.count(X)
        Ocount += row.count(O)

    if Xcount <= Ocount: # if x are few or equal
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    where i corresponds to the row of the move (0, 1, or 2) since its 3 by 3
    and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    all the moves you can make, all the mpty spaces where you can move, 
    Finds all the empty cells and returns them as a set of (row, column) tuples.
    """

    possible_moves = set() # defining a function actions that takes board as an input , its a set since it avoids using duplicates.

    for row_index, row in enumerate(board): # loop goes through the board row by row, enumerate gives index of the row and the actual row
        for column_index, item in enumerate(row):
            if item == None: #checck if the cell is empty
                possible_moves.add((row_index, column_index)) # if its empty then you add it's coordinates into set of possible moves 
    
    return possible_moves # the function returns the full set of all possible moves like {(0,2),(1,1)} etc


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
    like deep copy, also input is board(game state) and action (moves that you want to make)
    """
    player_move = player(board) # function calling 

    new_board = deepcopy(board) # getting a brand new board in memory without making the change in the og one
    i, j = action # row and col index

    if board[i][j] != None: # checks if the chosen cell is already filled 
        raise Exception # raises exception if illegal move , like ntohing will happen if you take the already occupied place 
    else:
        new_board[i][j] = player_move # if the spot is empty 

    return new_board # updated board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    """
    for player in (X, O):
        # check rows (horizontal)
        for row in board:
            if row == [player] * 3: # if a row is like [player, player, player] like [X,X,X] you win 
                return player

        # check columns (vertical)
        for i in range(3): # col num
            column = [board[r][i] for r in range(3)] # list, of each i-th col like i= 1, then col would be board [0][1], [1][1], [2][1]
            if column == [player] * 3: # check if it's matching
                return player

        # check diagonals
        if [board[i][i] for i in range(3)] == [player] * 3:
            return player
        if [board[i][2 - i] for i in range(3)] == [player] * 3:
            return player

    return None # no winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is won by one of the players
    if winner(board) != None: # if it returns the players option O OR X has and is NOT NONE means this condition is true 
        return True

    # moves still possible
    # if at leat one empty spot exist the game is not over yet so return false 
    for row in board:
        if EMPTY in row:
            return False
        

    return True # if there is no winner and no empty spaces means draw 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    assigns a score when the game is over this guides mini max decision making
    """

    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Using mini max algo. Refer to the notes!
    """

    def max_value(board): # Tries to maximize the score means: "X is playing and X wants the highest score."
        optimal_move = () # just sets up a placeholder for the best move found so far.
        if terminal(board): # 1, -1, 0
            return utility(board), optimal_move
        else:
            v = -5 # assign it to a low value outside the range of the possible outcome
            for action in actions(board): #Go through every possible move (action) available right now (all empty cells).
                minval = min_value(result(board, action))[0] #“If X does this, how will O (the minimizing player) respond?” call min_value.
                if minval > v: #If O’s best response still leaves X with a better score than what we’ve seen so far 
                    # update v and remember that move.
                    v = minval
                    optimal_move = action
            return v, optimal_move  #After trying all moves, return the best score X can get (v) and the move that leads to it

    def min_value(board): # for ex After trying all moves, return the best score X can get (v) and the move that leads to it.
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move # if game is over
        else:
            v = 5 #Start with a super high score, since O is trying to minimize.
            for action in actions(board):
                maxval = max_value(result(board, action))[0] #“If O does this, how will X (the maximizing player) respond?” → call max_value.
                if maxval < v:
                    v = maxval
                    optimal_move = action
            return v, optimal_move

    curr_player = player(board) #Figure out whose turn it is (X or O).

    if terminal(board): #If the game is already over, no move to make return None.
        return None
    #If it’s X’s turn → call max_value and return the move 
     #If it’s O’s turn → call min_value and return that move
    if curr_player == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]