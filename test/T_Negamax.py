# Testing Negamax Algorithm

from Negamax import Negamax, Negamax_AB

def test():
    'currently no error checking for valid user moves'

    N = Negamax()
    board = N.init_board()

    player = True
    while not N.game_over(board):
        if player: # black - AI
            print N.generate_black_moves(board)
            N.negamax(board, 2, 1) # -N.negamax(board, 2, -1)
            #N.negamax(board, 3, float('-inf'), float('inf'), 1)
            move = N.BEST_MOVE
            board = N.move_black(board, *move)
            N.print_board(board)
            player = False
        else:
            print N.generate_white_moves(board)
            i = int(raw_input("Enter piece i: "))
            j = int(raw_input("Enter piece j: "))
            i_new = int(raw_input("Enter new i: "))
            j_new = int(raw_input("Enter new j: "))
            board = N.move_white(board, (i, j), (i_new, j_new))
            N.print_board(board)
            player = True


def test_ab():
    'currently no error checking for valid user moves'

    N = Negamax_AB()
    board = N.init_board()

    player = True
    while not N.game_over(board):
        if player: # black - AI
            print N.generate_black_moves(board)
            #N.negamax(board, 2, 1) # -N.negamax(board, 2, -1)
            N.negamax(board, 3, float('-inf'), float('inf'), 1)
            move = N.BEST_MOVE
            board = N.move_black(board, *move)
            N.print_board(board)
            player = False
        else:
            print N.generate_white_moves(board)
            i = int(raw_input("Enter piece i: "))
            j = int(raw_input("Enter piece j: "))
            i_new = int(raw_input("Enter new i: "))
            j_new = int(raw_input("Enter new j: "))
            board = N.move_white(board, (i, j), (i_new, j_new))
            N.print_board(board)
            player = True


if __name__ == '__main__':

    test()
    # test_ab