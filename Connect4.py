""" Final code implements Monte Carlo Tree Search for board game Connect 4."""
"Credit to Jonathan A for Connect 4 and MCTS implementation"
"Credit to Nolan T for MinMax Implementation"
"Credit to Professor Kevin Gold for allowing me to use his MCTS framework for my Project"
"Credit to https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/ for providing pseudocode for MCTS"
"Credit to https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/ for pseudocode for Alpha Beta pruning MinMax "

import copy
from distutils.log import error
import sys
import numpy as np
MCTS_ITERATIONS =1000
NUM_COLS = 7
NUM_ROWS = 6
# With these constant values for players, flipping ownership is just a sign change
WHITE = 1
NOBODY = 0
BLACK = -1

TIE = 2  # An arbitrary enum for end-of-game

WHITE_TO_PLAY = True

# We'll sometimes iterate over this to look in all 8 directions from a particular square.
# The values are the "delta" differences in row, col from the original square.
# (Hence no (0,0), which would be the same square.)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def read_boardstring(boardstring):
    """Converts string representation of board to 2D numpy int array"""
    board = np.zeros((NUM_ROWS, NUM_COLS))
    board_chars = {
        'W': WHITE,
        'B': BLACK,
        '-': NOBODY
    }
    
    row = 0
    for line in boardstring.splitlines():
        for col in range(NUM_COLS):
            board[row][col] = board_chars.get(line[col], NOBODY) # quietly ignore bad chars
        row += 1

    return board

def find_winner(board):
    # Check rows for a winner
    #print("CHECKING FOR WINNER")
    for i in range(6):
        for j in range(4):
            #print(board[i][j])
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] and (board[i][j] == WHITE or board[i][j] == BLACK) :
                if board[i][j] == WHITE:
                    return WHITE
                elif board[i][j] == BLACK:
                    return BLACK
                else: 
                    print(board[i][j])
                    raise ValueError("Something is wrong....")
                    

    # Check columns for a winner
    for i in range(3):
        for j in range(7):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] and (board[i][j] == WHITE or board[i][j] == BLACK):
                if board[i][j] == WHITE:
                    return WHITE
                elif board[i][j] == BLACK:
                    return BLACK
                else: 
                    print(board[i][j])
                    raise ValueError("Something is wrong....")

    # Check diagonals for a winner (top-left to bottom-right)
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] and (board[i][j] == WHITE or board[i][j] == BLACK):
                if board[i][j] == WHITE:
                    return WHITE
                elif board[i][j] == BLACK:
                    return BLACK
                else: 
                    print(board[i][j])
                    raise ValueError("Something is wrong....")

    # Check diagonals for a winner (top-right to bottom-left)
    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] and (board[i][j] == WHITE or board[i][j] == BLACK):
                if board[i][j] == WHITE:
                    return WHITE
                elif board[i][j] == BLACK:
                    return BLACK
                else: 
                    print(board[i][j])
                    raise ValueError("Something is wrong....")

    # No winner found
    return TIE

def needs_one_move_to_win(board, player):
    """
    Want to find if the current player can win within one move
    """

    moves = generate_legal_moves(board,True)

    for move in moves:
       turn = True
       if player == BLACK:
            turn = False
       board_copy = play_move(board,move,turn) 
       #print_board(board_copy)
       if find_winner(board_copy) == player: 
            return True,move
    
    return False,None

def generate_legal_moves(board, white_turn):
    """Returns a list of (row, col) tuples representing places to move.

    Args:
        board (numpy 2D int array):  The board
        white_turn (bool):  True if it's white's turn to play
    """

    legal_moves = []
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS-1,-1,-1):
            if board[row][col] != NOBODY:
                continue   # Occupied, so not legal for a move
            # Legal moves must capture something
            legal_moves.append((row, col))
            break
    return legal_moves



def play_move(board, move, white_turn):
    """Handles the logic of putting down a new piece and flipping captured pieces.

    The board that is returned is a copy, so this is appropriate to use for search.

    Args:
        board (numpy 2D int array):  The board
        move ((int,int)):  A (row, col) pair for the move
        white_turn:  True iff it's white's turn
    Returns:
        board (numpy 2D int array)
    """
    new_board = copy.deepcopy(board)
    #print(move)
    new_board[move[0]][move[1]] = WHITE if white_turn else BLACK
    return new_board


def check_game_over(board):
    """Returns the current winner of the board - WHITE, BLACK, TIE, NOBODY"""

    # It's not over if either player still has legal moves
    white_legal_moves = generate_legal_moves(board, True)
    if white_legal_moves:  # Python idiom for checking for empty list
        return NOBODY
    black_legal_moves = generate_legal_moves(board, False)
    if black_legal_moves:
        return NOBODY
    # I guess the game's over
    return find_winner(board)


def print_board(board):
    """ Print board (and return None), for interactive mode"""
    print(board_to_string(board))
    
def board_to_string(board):
    printable = {
        -1: "B",
        0: "-",
        1: "W"
    }
    out = ""
    for row in range(NUM_ROWS):
        line = ""
        for col in range(NUM_COLS):
            line += printable[board[row][col]]
        out += line + "\n"
    return out




def play():
    """Interactive play, for demo purposes.  Assume AI is white and goes first."""
    print("1 for vs MCTS")
    print("2 for vs MinMax")
    print("3 for BOT VS BOT")

    choice = int(input())
    if choice != 1 and choice != 2 and choice != 3:
         print("please type a number between 1 2 3. Shutting Down")
         return
    board = starting_board()
    white_turn = random.random() > 0.5   #switch for whoever goes first
    print(white_turn)
    while find_winner(board) == TIE:
        # White turn (MCTS AI_  

        legal_moves = generate_legal_moves(board, True)
        if legal_moves:  # (list is non-empty)
            if white_turn and (choice == 1 or choice == 3):
                print("MCTS IS THINKING...")
                best_move = MCTS_choice(board, True, MCTS_ITERATIONS)  #this is turned on if we want the bot to take a turn          
                #best_move = get_player_move(board, legal_moves) #using another player for now
                board = play_move(board, best_move, True)
                white_turn = not white_turn
                print_board(board)
                #print("")
                if find_winner(board) != TIE:
                    print("we have a winner")
                    print_board(board)
                    break
            elif white_turn and choice == 2:
                 print("Your turn buddy")                          
                 best_move = get_player_move(board, legal_moves) #using another player for now
                 board = play_move(board, best_move, True)
                 white_turn = not white_turn
                 print_board(board)
                 #print("")
                 if find_winner(board) != TIE:
                    print("we have a winner")
                    print_board(board)
                    break
        else:
            print("White has no legal moves; ending game")
            break

        legal_moves = generate_legal_moves(board, False)
        if legal_moves :
            #BLACK TURN (MINMAX AI)

            if not white_turn and (choice == 2 or choice == 3):
                #player_move = get_player_move(board, legal_moves)  #change to this if u want a player vs MCTS 
                #--------------
                print("MINIMAX TURN")
                tempboard = copy.deepcopy(board)        
                tempboard= np.flip(tempboard,0)
                col, minimax_score = minimax(tempboard, 5, -math.inf, math.inf, True)

                #print("minmax is done thinking")
                #print(col)
                
                row = -1
                moves = generate_legal_moves(board,False)
                
                for m in moves:
                     if col == m[1]:
                          row = m[0]
                          break
                tuple = (row,col)



                board = play_move(board,tuple,False)   

                #board = play_move(board, player_move, False)   #for player moves
                print_board(board)
                white_turn = not white_turn
                if find_winner(board) != TIE:
                    print("we have a winner")
                    print_board(board)
                    break
            elif not white_turn and choice == 1:
                player_move = get_player_move(board, legal_moves)  #change to this if u want a player vs MCTS 
                #--------------
                print("Your Turn")
                board = play_move(board,player_move,False)   
                print_board(board)
                white_turn = not white_turn
                if find_winner(board) != TIE:
                    print("we have a winner")
                    print_board(board)
                    break                    
        else:
            print("Black has no legal moves; ending game")
            break
    winner = find_winner(board)
    if winner == WHITE:
        print("White won!")
    elif winner == BLACK:
        print("Black won!")
    else:
        print("Tie!")

def starting_board():
    """Returns a board with the traditional starting positions in Othello."""
    board = np.zeros((NUM_ROWS, NUM_COLS))

    return board

def get_player_move(board, legal_moves):
    """Print board with numbers for the legal move spaces, then get player choice of move

    Args:
        board (numpy 2D int array):  The Othello board.
        legal_moves (list of (int,int)):  List of legal (row,col) moves for human player
    Returns:
        (int, int) representation of the human player's choice
    """
    for row in range(NUM_ROWS):
        line = ""
        for col in range(NUM_COLS):
            if board[row][col] == WHITE:
                line += "W"
            elif board[row][col] == BLACK:
                line += "B"
            else:
                if (row, col) in legal_moves:
                    line += str(legal_moves.index((row, col)))
                else:
                    line += "-"
        print(line)
    while True:
        # Bounce around this loop until a valid integer is received
        choice = input("Which move do you want to play? [0-" + str(len(legal_moves)-1) + "]")
        try:
            move_num = int(choice)
            if 0 <= move_num < len(legal_moves):
                return legal_moves[move_num]
            print("That wasn't one of the options.")
        except ValueError:
            print("Please enter an integer as your move choice.")


class MCTSNode:
  def __init__(self, parent, move, board, white_turn):
    self.parent = parent
    self.children = []
    self.white_turn = white_turn
    self.move = move
    self.board = board
    self.playouts = 0
    self.wins = 0
  
  def __str__(self): # Can modify this for debugging purposes
    s = board_to_string(self.board)
    if self.move is not None:
      s += str(self.move[0]) + "," + str(self.move[1])
    s += "\n" + str(self.wins) + "/" + str(self.playouts) + "\n"
    return s
  
import math

def UCB1(node):
  #TODO  
    return node.wins/node.playouts + math.sqrt(2) * (math.sqrt((math.log(node.parent.playouts)) /(node.playouts) ) )
    
def UCT(nodelist):
    bestnodeval = UCB1(nodelist[0])
    bestnode = nodelist[0]
    for n in nodelist:
        if UCB1(n)>bestnodeval:
            bestnodeval = UCB1(n)
            bestnode = n
        
    return bestnode

def selection(root):
  # TODO
  
    traverse = root 
    foundchild = False
    while foundchild != True:
        count1 = len(generate_legal_moves(traverse.board,traverse.white_turn))
        if count1 == 0:  #pass turn if the legal moves is  0
            #print("this is stupid")
            return traverse,[]
        count2 = len(traverse.children)
        
        if(count1 == count2):   #if all children good then choose the children with the highest UBC1  
            traverse = UCT(traverse.children)
        else:   #if not all children good, then return 
            foundchild = True
            #print(generate_legal_moves(traverse.board,traverse.white_turn))
            return traverse,generate_legal_moves(traverse.board,traverse.white_turn)   
        
def expansion(parent, possible_children):
  random.shuffle(possible_children) 
  for move in possible_children:
    board = play_move(parent.board, move, parent.white_turn)
    child = MCTSNode(parent, move, board, not parent.white_turn)
    if not any(movedChild.move == move for movedChild in parent.children):
        parent.children.append(child)

        return child
  return parent

import random

def simulation(node):
  # TODO
    
    trav = node.board

    # print("------------------------SIMULATION---------------------------------")
    # print(node.white_turn)
    # print_board(node.board)

    turn = node.white_turn
    if find_winner(trav) == WHITE:
        return True
    if find_winner(trav) == BLACK: 
        return False
    while len(generate_legal_moves(trav,turn))>0 or len(generate_legal_moves(trav,not turn))>0:
        if(len(generate_legal_moves(trav,turn)) == 0): 
            return False                #if there are no legal moves then game is over
        else:
            #print(trav)
            #if turn == True and needs_one_move_to_win(trav, WHITE) == True: 
            #          return True
            if turn == False and needs_one_move_to_win(trav, BLACK)[0] == True:
                      return False
            else:
                rando = random.randint(0,len(generate_legal_moves(trav,turn))-1)
                movetoplay = generate_legal_moves(trav,turn)[rando]
                trav = play_move(trav,movetoplay,turn )
            
            turn = not turn  #give the other player a turn
            #print(node.white_turn)
     

        if find_winner(trav) == WHITE:
            # print("done")
            # print("WHITE WIN")
            # print(turn)
            # print_board(trav)
            
            return True
        elif find_winner(trav) == BLACK:
            # print("done")
            # print(turn)
            # print_board(trav)
            return False
    
    if find_winner(trav) == WHITE:
            # print("done")
            # print("WHITE WIN")
            # print(turn)
            # print_board(trav)
            return True
    else:
            # print("done")
            # print(turn)
            # print_board(trav)
            return False
    
def backpropagation(node, white_win):
    while node is not None: 
        node.playouts = node.playouts + 1  
        if white_win == 1:
                node.wins = node.wins +1
        node = node.parent
    


def MCTS_choice(board, white_turn, iterations):
  pre = needs_one_move_to_win(board, BLACK)
  #print(pre[0])
  #print(pre[1])
  if pre[0] == True:
     return pre[1]  
  start_node = MCTSNode(None,None,board,white_turn)
  for i in range(iterations):

    current_node, possible_children = selection(start_node)
    
    new_node = expansion(current_node, possible_children)
   
    white_win = simulation(new_node)
    backpropagation(new_node, white_win)
  # We look for the start node that has the most playouts -
  # not win % because this way favors nodes that have been tried quite a bit
  # (and are also good, or they wouldn't have been tried)

  max_playouts = -1000000
  best_child = None
  for child in start_node.children:

    # print(child.move)
    # print(child.playouts)
    # print(child.wins)
    if child.playouts > max_playouts:
      max_playouts = child.playouts
      best_child = child
#   print("done")
#   print(best_child.move)
  
  return best_child.move  

#--------------------------------------END OF Jonathans part of code-------------------------------------------------------------------------------------------------------


def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[NUM_ROWS-1][col] == 0

def get_next_open_row(board, col):
	for r in range(NUM_ROWS):
		if board[r][col] == 0:
			return r
                
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(NUM_COLS):
		for r in range(NUM_ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(NUM_COLS-3):
		for r in range(NUM_ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(NUM_COLS-3):
		for r in range(3, NUM_ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = WHITE


	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(NOBODY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(NOBODY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(NOBODY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, NUM_COLS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(NUM_ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(NUM_COLS-3):
			window = row_array[c:c+4]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(NUM_COLS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(NUM_ROWS-3):
			window = col_array[r:r+4]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(NUM_ROWS-3):
		for c in range(NUM_COLS-3):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	for r in range(NUM_ROWS-3):
		for c in range(NUM_COLS-3):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, WHITE) or winning_move(board, BLACK) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, BLACK):
                return (None, 100000000000000)
            elif winning_move(board, WHITE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, BLACK))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, BLACK)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, WHITE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(NUM_COLS):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations


play()
# board = np.zeros((NUM_ROWS, NUM_COLS))

# board[2][3] = BLACK
# board[3][4] = BLACK
# board[4][5] = 0
# board[5][5] = BLACK
# board[5][6] = BLACK
# print(board)
# print(needs_one_move_to_win(board,BLACK))
