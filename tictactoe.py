"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter_o = 0
    counter_x = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                counter_x += 1
            elif board[i][j] == O:
                counter_o += 1
        
    if counter_x == counter_o:
        return X
    
    elif counter_x > counter_o:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create a set then store all the empty positions as potential actions
    list_actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])): 
            if board[i][j] == None:
                list_actions.add((i, j))
    return list_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # if invalid action then raise exception
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    # create deep copy so don't alter origional board
    deep_copy_board = [row[:] for row in board]
    # makes the board from the proposed action (i, j)
    deep_copy_board[action[0]][action[1]] = player(board)
    
    return deep_copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # index into the boards to find if any have three in a row

    for i in range(3):
        # check rows 
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] != None:
                return board[i][0]
        
        # check columns
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] != None:
                return board [0][i]
        
    # check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] != None:
            return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] != None:
            return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # check if there is already a winner
    if winner(board) != None:
        return True 
    
    # check if any moves are still to play
    else:
        for row in board:
            for cell in row:
                if cell == None:
                    return False 
        return True
  

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    move = None
    # use alpha and beta so can do alpha-beta pruning
    alpha, beta = -math.inf, math.inf
    if player(board) == X:
        # set the best value so far from a minimizer 
        best = -math.inf
        # check the child nodes 
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            alpha = max(alpha, value)
            # pruning 
            if best < value:
                best = value
                move = action 
        return move

    else:
        best = math.inf
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            beta = min(beta, value)
            if value < best:
                best = value
                move = action
    return move 


def max_value(board, alpha, beta):
    """
    Returns the maximum value move to choose 
    """
    # return the winning value if the game is over
    if terminal(board):
        return utility(board)
    best = -math.inf
    for action in actions(board):
        best = max(best, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, best)
        if beta <= alpha:
            break
    return best


def min_value(board, alpha, beta):
    """
    Returns the minimum value move to choose 
    """
    if terminal(board):
        return utility(board)
    best = math.inf
    for action in actions(board):
        best = min(best, max_value(result(board, action), alpha, beta))
        beta = min(beta, best)
        if beta <= alpha:
            break
    return best 

