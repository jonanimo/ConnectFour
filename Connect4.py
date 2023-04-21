""" Final code implements Monte Carlo Tree Search for board game Connect 4."""
"Credit to Professor Kevin Gold for allowing me to use his framework for my Project"
"Credit to https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/ for providing pseudocode for MCTS"
import copy
import sys
import numpy as np

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

def find_winner(board,last_move_row,last_move_col):
    """Return identity of winner, assuming game is over.

    Args:
        board (numpy 2D int array):  The othello board, with WHITE/BLACK/NOBODY in spaces

    Returns:
        int constant:  WHITE, BLACK, or TIE.
    """
    # Slick counting of values:  np.count_nonzero counts vals > 0, so pass in
    #we gotta count in all 4 directions
    whatcolor = board[last_move_row][last_move_col]         #getting the color of the lastmoveplayed to try and find a winner
    win = 0
  
    num = 1 #number of chips in a row
    #check left anf right first
    if last_move_col < len(board[0])-1:
        for i in range(last_move_col+1,len(board[0])):
            if ( board[last_move_row][i] == whatcolor):
                num = num + 1
            else: break
    if last_move_col > 0:
        for i in range(last_move_col-1,-1,-1):
            if ( board[last_move_row][i] == whatcolor):
                num = num + 1
            else: break
    if num >= 4:
        if whatcolor == WHITE:
            return WHITE
        else: return BLACK

    num = 1 #number of chips in a row
    #check up and down
    if last_move_row < len(board)-1:
        for i in range(last_move_row+1,len(board)):
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break
    if last_move_row > 0:
        for i in range(last_move_row-1,-1,-1):
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break
    if num >= 4:
        if whatcolor == WHITE:
            return WHITE
        else: return BLACK

    num = 1 #number of chips in a row
    #checking in this direction "/"
    if last_move_row < len(board)-1 and last_move_col < len(board[0])-1:
        for i in range(last_move_row+1,len(board)):
            last_move_col = last_move_col + 1
            if(last_move_col >= len(board[0])): #edge case in case we reached the column boundary 
                break
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break
    if last_move_row > 0 and last_move_col > 0 :
        for i in range(last_move_row-1,-1,-1):
            last_move_col = last_move_col -1
            if last_move_col <= -1:             #same edge case for reaching boundary, row will not reach it because it is what we sue for range
                break
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break
    if num >= 4:
        if whatcolor == WHITE:
            return WHITE
        else: return BLACK

    num = 1 #number for chips 
    #checking this direction "\"
    if last_move_row < len(board)-1 and last_move_col >0:   #first we check the up and left direction
        for i in range(last_move_row+1,len(board)):
            last_move_col = last_move_col - 1 
            if last_move_col <= -1: 
                break
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break
    
    if last_move_row > 0 and last_move_col < len(board[0])-1:
        for i in range(last_move_row-1,-1,-1):
            last_move_col = last_move_col + 1
            if last_move_col >= len(board[0]):             #same edge case for reaching boundary, row will not reach it because it is what we sue for range
                break
            if ( board[i][last_move_col] == whatcolor):
                num = num + 1
            else: break

    if num >= 4:
        if whatcolor == WHITE:
            return WHITE
        else: return BLACK        

    return TIE

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

MCTS_ITERATIONS = 1000

def play():
    gameboard = starting_board()
    board= """-------
-------
-------
-------
-------
WWW----"""
    my_root = MCTSNode(None, None, read_boardstring(board), True)
    my_root.playouts = 6
    my_root.wins = 2
    children_moves = generate_legal_moves(read_boardstring(board),True)
    children = []
    for move in children_moves:
      new_board = play_move(my_root.board,move,True)
      node = MCTSNode(my_root,move,new_board,False)
      node.playouts = 2
      node.wins = 1
      children.append(node)
    children[3].wins = 2 # The best move happens to be the first move listed
    my_root.children = children
    # Now test UCB1 on each, and UCT to select the best
    for child in my_root.children:
      print(UCB1(child))  # Expect about 2.34 for first, 1.84 for other two
    print(UCT(my_root.children)) # Expect the node with 2/2 wins
    children_moves = generate_legal_moves(read_boardstring(board),True)
    print(children_moves)
#     """Interactive play, for demo purposes.  Assume AI is white and goes first."""
    node, children = selection(my_root)
    print(node) # Expect the node with 2/2 wins
    print(children) # Expect [(2, 3), (3, 2), (4, 5), (5, 4)]
    
 
    
   
#     while check_game_over(board) == NOBODY:
#         # White turn (AI)
#         lastmove = (-1,-1)
#         legal_moves = generate_legal_moves(board, True)
#         if legal_moves:  # (list is non-empty)
#             print("Thinking...")
#             best_move = MCTS_choice(board, True, MCTS_ITERATIONS)
#              #this is turned on if we want the bot to take a turn0
            
#             #best_move = get_player_move(board, legal_moves) #using another player for now
#             board = play_move(board, best_move, True)
#             #print_board(board)
#             #print("")
#             lastmove = best_move
#             if find_winner(board,best_move[0],best_move[1]) != TIE:
#                 print("we have a winner")
#                 print_board(board)
#                 break
#         else:
#             print("White has no legal moves; skipping turn...")

#         legal_moves = generate_legal_moves(board, False)
#         if legal_moves:
#             player_move = get_player_move(board, legal_moves)
#             board = play_move(board, player_move, False)
#             print_board(board)
#             lastmove = player_move
#             if find_winner(board,player_move[0],player_move[1]) != TIE:
#                 print("we have a winner")
#                 print_board(board)
#                 break
#         else:
#             print("Black has no legal moves; skipping turn...")
#     winner = find_winner(board,lastmove[0],lastmove[1])
#     if winner == WHITE:
#         print("White won!")
#     elif winner == BLACK:
#         print("Black won!")
#     else:
#         print("Tie!")

def starting_board():
     """Returns a board with the traditional starting positions in Othello."""
     board = np.zeros((NUM_ROWS, NUM_COLS))

     return board

# def get_player_move(board, legal_moves):
#     """Print board with numbers for the legal move spaces, then get player choice of move

#     Args:
#         board (numpy 2D int array):  The Othello board.
#         legal_moves (list of (int,int)):  List of legal (row,col) moves for human player
#     Returns:
#         (int, int) representation of the human player's choice
#     """
#     for row in range(NUM_ROWS):
#         line = ""
#         for col in range(NUM_COLS):
#             if board[row][col] == WHITE:
#                 line += "W"
#             elif board[row][col] == BLACK:
#                 line += "B"
#             else:
#                 if (row, col) in legal_moves:
#                     line += str(legal_moves.index((row, col)))
#                 else:
#                     line += "-"
#         print(line)
#     while True:
#         # Bounce around this loop until a valid integer is received
#         choice = input("Which move do you want to play? [0-" + str(len(legal_moves)-1) + "]")
#         try:
#             move_num = int(choice)
#             if 0 <= move_num < len(legal_moves):
#                 return legal_moves[move_num]
#             print("That wasn't one of the options.")
#         except ValueError:
#             print("Please enter an integer as your move choice.")


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

    #print("---------------------------------------------------------")
    while len(generate_legal_moves(trav,node.white_turn))>0 or len(generate_legal_moves(trav,not node.white_turn))>0:
        if(len(generate_legal_moves(trav,node.white_turn)) == 0): #let the other player go because there are no legal moves
            return False                #changed this to return False because if there are no legal moves game ends unlike Othello
        else:
            rando = random.randint(0,len(generate_legal_moves(trav,node.white_turn))-1)
            movetoplay = generate_legal_moves(trav,node.white_turn)[rando]
            

            trav = play_move(trav,movetoplay,node.white_turn )

            node.white_turn = not node.white_turn  #give the other player a turn
            #print(node.white_turn)
     

        if find_winner(trav,movetoplay[0],movetoplay[1]) == WHITE:
            #print("done")
            #print_board(trav)
            
            return True
        elif find_winner(trav,movetoplay[0],movetoplay[1]) == BLACK:
            #print_board(trav)
            return False
    
    if find_winner(trav,movetoplay[0],movetoplay[1]) == WHITE:
        #print_board(trav)
        return True
    else:
        #print_board(trav)
        return False
    
def backpropagation(node, white_win):
    while node is not None:
        node.playouts = node.playouts +1   
        if white_win == 1:
            if node.white_turn == False:
                node.wins = node.wins +1
        node = node.parent

def MCTS_choice(board, white_turn, iterations):

  start_node = MCTSNode(None,None,board,white_turn)
  for i in range(iterations):

    current_node, possible_children = selection(start_node)
    
    new_node = expansion(current_node, possible_children)
   
    white_win = simulation(new_node)
    backpropagation(new_node, white_win)
  # We look for the start node that has the most playouts -
  # not win % because this way favors nodes that have been tried quite a bit
  # (and are also good, or they wouldn't have been tried)


  max_playouts = 0
  best_child = None
  for child in start_node.children:
    #2print(child.move)0

    if child.playouts > max_playouts:
      max_playouts = child.playouts
      best_child = child
  print("done")
  return best_child.move  

play()
#Test 1 should return false because its basically all black
# filled_board = """-------
# -------
# -------
# -------
# -------
# W-WW---"""
#my_root2 = MCTSNode(None, None, read_boardstring(filled_board), True)
#print(read_boardstring(filled_board))
#my_root2.playouts = 2
#my_root2.wins = 2
#children_moves = generate_legal_moves(read_boardstring(filled_board),True)
#children = []
#for move in children_moves: # Should be only one
  #new_board = play_move(my_root2.board,move,True)
 # node = MCTSNode(my_root2,move,new_board,False)
 # node.playouts = 2
 # node.wins = 0
#  children.append(node)
#my_root2.children = children

#winner = simulation(my_root2)
#print(winner)