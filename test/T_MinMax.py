# Testing MinMax Algorithm

from MinMax import MinMax

def test():
    'currently no error checking for valid user moves'

    mm = MinMax()
    board = mm.init_board()

    player = True
    while not mm.game_over(board):
        if player: # black - AI
            print mm.generate_black_moves(board)
            mm.minmax(board, 2, False) # don't know why False
            move = mm.BEST_MOVE
            board = mm.move_black(board, *move)
            mm.print_board(board)
            player = False
        else:
            print mm.generate_white_moves(board)
            i = int(raw_input("Enter piece i: "))
            j = int(raw_input("Enter piece j: "))
            i_new = int(raw_input("Enter new i: "))
            j_new = int(raw_input("Enter new j: "))
            board = mm.move_white(board, (i, j), (i_new, j_new))
            mm.print_board(board)
            player = True


if __name__ == '__main__':

    test()