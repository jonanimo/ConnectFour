import numpy as np

def createboard():
    board = np.zeros((6,7))
    return board

board = createboard()

game_over = False
turn = 0

while not game_over():
    if turn == 0:
        selection = int(input("Player 1"))
        turn += 1
    else:
        selection = int(input("Player 2"))
        turn -= 1

