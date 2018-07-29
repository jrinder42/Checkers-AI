# Testing AlphaBeta Algorithm

from AlphaBeta import AlphaBeta

def test():
    'currently no error checking for valid user moves'

    AB = AlphaBeta()
    board = AB.init_board()

    player = True
    while not AB.game_over(board):
        if player: # black - AI
            print AB.generate_black_moves(board)
            AB.alphabeta(board, 6, float('-inf'), float('inf'), False) # don't know why False
            move = AB.BEST_MOVE
            board = AB.move_black(board, *move)
            AB.print_board(board)
            player = False
        else:
            print AB.generate_white_moves(board)
            i = int(raw_input("Enter piece i: "))
            j = int(raw_input("Enter piece j: "))
            i_new = int(raw_input("Enter new i: "))
            j_new = int(raw_input("Enter new j: "))
            board = AB.move_white(board, (i, j), (i_new, j_new))
            AB.print_board(board)
            player = True


if __name__ == '__main__':

    test()