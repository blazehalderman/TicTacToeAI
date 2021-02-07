"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    #X ALWAYS gets first move, alternates with each additional move
    curr_moves = actions(board)
    if (board == initial_state()):
        return X
    if(len(curr_moves) % 2 == 0):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []

    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                moves.append((i, j))
    return(moves)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    # places the action on the board for a specific player
    try:
        if board_copy[action[0]][action[1]] != EMPTY:
            raise Exception("Invalid action")
        else:
            board_copy[action[0]][action[1]] = player(board_copy)
            return board_copy
    except IndexError:
        print("Spot occupied")

#BROKEN HERE
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # finite list of possible wins
    winnings = [
        (0, 0), (0, 1), (0, 2), 
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 0), (1, 1), (2, 2),
        (2, 0), (1, 1), (0, 2)
    ]
    # if the board has one of the lists in winnings 
    #   then the piece in one of those spots is the winner
    xcount = 0
    ocount = 0
    for i in range(len(winnings)):
        if(board[winnings[i][0]][winnings[i][1]] == X):
                xcount += 1
        if(board[winnings[i][0]][winnings[i][1]] == O):
                ocount += 1
        if((i + 1) % 3 == 0):
            if(ocount == 3 or xcount == 3):
                return board[winnings[i][0]][winnings[i][1]]
            else:
                ocount = 0
                xcount = 0
    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    curr_moves = actions(board)
    #tie
    if(len(curr_moves) == 0 and winner(board) == EMPTY):
        return True
    #winner
    elif(len(curr_moves) != 0 and winner(board) != EMPTY):
        return True
    #game on
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # if game is over (tie/winner) decide who won
    if(terminal(board)):
        if(winner(board) == X):
            return 1
        elif(winner(board) == O):
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if(terminal(board)):
        return None

    if (board == initial_state()):
        x = random.choice([0, 2])
        y = random.choice([0, 2])
        return(x, y)

    if(current_player == X):
        v = -math.inf
        for action in actions(board):
            mini = min_value(result(board, action))
            if mini > v:
                v = mini
                best_move = action
    else:
        v = math.inf
        for action in actions(board):
            maxi = max_value(result(board, action))
            if maxi < v:
                v = maxi
                best_move = action
    return best_move

def max_value(board):
    if(terminal(board)):
        return(utility(board))
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if(terminal(board)):
        return(utility(board))
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

