import numpy as np
import math

ROWS = 6
COLS = 7

# Create the Connect Four board
def create_board():
    board = np.zeros((ROWS,COLS))
    return board

# Print the Connect Four board
def print_board(board):
    print(np.flip(board, 0))

# Check if a move is valid
def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

# Get the next open row for a move
def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

# Drop a piece onto the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_tie_game(board):
    for col in range(COLS):
        if is_valid_location(board, col):
            return False
    return True

# Check if a move wins the game
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check diagonal locations for win
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Evaluate the score of the board for a player
def evaluate(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score diagonal positive slope
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score diagonal negative slope
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Evaluate the score of a window of 4 cells
def evaluate_window(window, piece):
    opp_piece = 1
    if piece == 1:
        opp_piece = 2

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

# Get the list of valid moves
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Minimax algorithm for the AI player
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = len(valid_locations) == 0 or depth == 0
    if is_terminal:
        if winning_move(board, 2):
            return (None, 100000000000000)
        elif winning_move(board, 1):
            return (None, -10000000000000)
        else:
            return (None, 0)

    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Main function for the game
def main():
    # Create the board
    board = create_board()
    print_board(board)

    # Set the first player
    turn = 1

    # Start the game loop
    game_over = False
    while not game_over:
        # Ask for the player's move
        if turn == 1:
            col = int(input("Player 1 make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)
                if winning_move(board, turn):
                    print("Player 1 wins!")
                    game_over = True

        # AI player makes its move
        else:
            col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)
                if winning_move(board, turn):
                    print("AI player wins!")
                    game_over = True

        # Print the board
        print_board(board)

        # Switch the turn
        turn = 1 if turn == 2 else 2

        # Check for a tie game
        if is_tie_game(board):
            print("Tie game!")
            game_over = True

# Call the main function to start the game
if __name__ == '__main__':
    main()

