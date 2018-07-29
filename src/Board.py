class Board:

    #MAXDEPTH = 4

    def __init__(self):
        '''
        :return: nothing
        '''
        self.board = []
        self.white_pieces = []
        self.black_pieces = []

    def init_board(self):
        '''
        :return: initializes board
        '''
        board = [[0 for _ in xrange(8)] for _ in xrange(8)]
        for i in xrange(3):
            for j in xrange(8):
                if (i + j) % 2 == 0:
                    board[i][j] = -1 # black
                if abs(-(i + 1) + -(j + 1)) % 2 == 0:
                    board[-(i + 1)][-(j + 1)] = 1 # white
        return board

    '''
    def init_white(self, board):

        :return: nothing - creates white piece list

        #board = self.init_board()
        self.white_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == 1]

    def init_black(self, board):

        :return: nothing - creates black piece list

        #board = self.init_board()
        self.black_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == -1]
    '''

    def get_white_pieces(self, board):
        '''
        :return: white piece list
        '''
        #self.white_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == 1]
        #return self.white_pieces
        white_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == 1 or board[i][j] == 2]
        return white_pieces

    def get_black_pieces(self, board):
        '''
        :return: black piece list
        '''
        #self.black_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == -1]
        #return self.black_pieces
        black_pieces = [(i, j) for j in xrange(8) for i in xrange(8) if board[i][j] == -1 or board[i][j] == -2]
        return black_pieces

    '''
    def set_white_piece(self, old_pos, new_pos, board):

        :param old_pos: current piece position
        :param new_pos: position the piece will be moved to
        :return: new white piece list

        # check if white piece
        board[new_pos[0]][new_pos[1]] = board[old_pos[0]][old_pos[1]]
        board[old_pos[0]][old_pos[1]] = 0 # updating board
        return board

    def set_black_piece(self, old_pos, new_pos, board):

        :param old_pos: current piece position
        :param new_pos: position the piece will be moved to
        :return: new black piece list

        # check if black piece
        board[new_pos[0]][new_pos[1]] = board[old_pos[0]][old_pos[1]]
        board[old_pos[0]][old_pos[1]] = 0 # updating board
        return board
    '''

    def remove_white_piece(self, position, board):
        '''
        :param position: white piece to remove
        :return: new white piece list
        '''
        board[position[0]][position[1]] = 0
        return board

    def remove_black_piece(self, position, board):
        '''
        :param position: black piece to remove
        :return: new black piece list
        '''
        board[position[0]][position[1]] = 0
        return board

    def print_board(self, board):
        '''
        :return: nothing - prints current board
        '''
        for i in xrange(8):
            item = []
            print str(8 - i),
            for j in xrange(8):
                if board[i][j] == -1: # black
                    item.append(u'\u25CF')
                elif board[i][j] == -2:
                    item.append(u'\u25A0')
                elif board[i][j] == 1: # white
                    item.append(u'\u25CB')
                elif board[i][j] == 2:
                    item.append(u'\u25A1')
                else: # open
                    item.append(u'\u00B7')
            print ' '.join(item)
        print '  a b c d e f g h'


'''
Functional Flow Diagram

--> indicates the statement 'is used in'

boundary_check --> is_open

_create_king_white --> is_king

_create_king_black --> is_king
'''

class Actions(Board):

    def __init__(self):
        '''
        :return: nothing
        '''
        Board.__init__(self)

    def boundary_check(self, position):
        '''
        :param move: (row, column)
        :return: boolean of whether the position is out of bounds of the board
        '''
        if position[0] >= 0 and position[1] >= 0 and position[0] < 8 and position[1] < 8:
            return True
        return False

    def is_open(self, position, move, board):
        '''
        :param position: (row, column)
        :param move: (1, 1) or (1, -1) or (-1, 1) or (-1, -1) - specific to white or black
        :return: boolean of whether the move is valid/
        '''
        x = position[0] + move[0]
        y = position[1] + move[1]
        future_position = (x, y)
        if self.boundary_check(future_position) and board[x][y] == 0:
            return (True, future_position) # only use future_position here
        return (False, future_position)

    def valid_white_moves(self):
        '''
        :return: valid white moves
        '''
        return {(-1, 1), (-1, -1)}

    def valid_black_moves(self):
        '''
        :return: valid black moves
        '''
        return {(1, -1), (1, 1)}

    def valid_king_moves(self):
        '''
        :return: valid king moves
        '''
        return {(1, 1), (1, -1), (-1, 1), (-1, -1)} # Set

    def is_king(self, position, player, board):
        '''
        :param position: current player position
        :param player: 0-white, 1-black
        :return: boolean
        '''
        if not player: # white
            board = self._create_king_white(position, board)
            if board[position[0]][position[1]] == 2:
                return True
        else:
            board = self._create_king_black(position, board)
            if board[position[0]][position[1]] == -2:
                return True
        return False

    def _create_king_white(self, position, board):
        '''
        :param position: current player position
        :return: boolean
        '''
        if position[0] == 0:
            board[position[0]][position[1]] = 2
        return board

    def _create_king_black(self, position, board):
        '''
        :param position: current player position
        :return: boolean
        '''
        if position[0] == 7:
            board[position[0]][position[1]] = -2
        return board

    def generate_white_moves(self, board):
        '''
        :return: generator - yields (current piece, future position of piece, bool indicating if piece jumps)
        '''
        positions = []
        for piece in self.get_white_pieces(board):
            if self.is_king(piece, 0, board):
                for move in self.valid_king_moves():
                    is_available, position = self.is_open(piece, move, board)
                    if is_available:
                        positions.append((piece, position))
                        #yield (piece, position)
                    else: # jump
                        x = piece[0] + move[0]
                        y = piece[1] + move[1]
                        future_position = (x, y)
                        is_available, position = self.is_open(future_position, move, board)
                        if is_available and future_position in self.get_black_pieces(board):
                            positions.append((piece, position))
                            #yield (piece, position)
            else:
                for move in self.valid_white_moves():
                    is_available, position = self.is_open(piece, move, board)
                    if is_available:
                        positions.append((piece, position))
                        #yield (piece, position)
                    else:
                        x = piece[0] + move[0]
                        y = piece[1] + move[1]
                        future_position = (x, y)
                        is_available, position = self.is_open(future_position, move, board)
                        if is_available and future_position in self.get_black_pieces(board):
                            positions.append((piece, position))
                            #yield (piece, position)
        return positions

    def generate_black_moves(self, board):
        '''
        :return: generator - yields (current piece, future position of piece, bool indicating if piece jumps)
        '''
        positions = []
        for piece in self.get_black_pieces(board):
            if self.is_king(piece, 1, board):
                for move in self.valid_king_moves():
                    is_available, position = self.is_open(piece, move, board)
                    if is_available:
                        positions.append((piece, position))
                        #yield (piece, position)
                    else: # jump
                        x = piece[0] + move[0]
                        y = piece[1] + move[1]
                        future_position = (x, y)
                        is_available, position = self.is_open(future_position, move, board)
                        if is_available and future_position in self.get_white_pieces(board):
                            positions.append((piece, position))
                            #yield (piece, position)
            else:
                for move in self.valid_black_moves():
                    is_available, position = self.is_open(piece, move, board)
                    if is_available:
                        positions.append((piece, position))
                        #yield (piece, position)
                    else:
                        x = piece[0] + move[0]
                        y = piece[1] + move[1]
                        future_position = (x, y)
                        is_available, position = self.is_open(future_position, move, board)
                        if is_available and future_position in self.get_white_pieces(board):
                            positions.append((piece, position))
                            #yield (piece, position)
        return positions

    def update_board(self, old_pos, new_pos, to_remove, board):
        '''
        :param old_pos: current position of piece
        :param new_pos: future position of the piece
        :param to_remove: bool indicating if we remove the piece or not - special case
        :return: nothing - updates board
        '''
        if not to_remove:
            board[new_pos[0]][new_pos[1]] = board[old_pos[0]][old_pos[1]] # update board
            board[old_pos[0]][old_pos[1]] = 0
        else:
            board[old_pos[0]][old_pos[1]] = 0
        return board

    def move_white(self, board, old_pos, new_pos):
        '''
        :param old_pos: current position of piece
        :param new_pos: future position of piece
        :return: nothing - moves piece and updates board
        '''
        move_x = new_pos[0] - old_pos[0]
        move_y = new_pos[1] - old_pos[1]
        move = (move_x, move_y)
        if self.is_open(old_pos, move, board)[0]: # new_pos
            new_board = self.update_board(old_pos, new_pos, 0, board)

            #self.set_white_piece(old_pos, new_pos)

            if abs(move_x) % 2 == 0:
                middle_move = (move_x / 2, move_y / 2)
                middle_position_x = old_pos[0] + middle_move[0]
                middle_position_y = old_pos[1] + middle_move[1]
                middle_position = (middle_position_x, middle_position_y)
                new_board = self.remove_black_piece(middle_position, new_board)
                new_board = self.update_board(middle_position, middle_position, 1, new_board)
            return new_board
        else:
            raise ValueError('Invalid Move')

    def move_black(self, board, old_pos, new_pos):
        '''
        :param old_pos: current position of piece
        :param new_pos: future position of piece
        :return: nothing - moves piece and updates board
        '''
        move_x = new_pos[0] - old_pos[0]
        move_y = new_pos[1] - old_pos[1]
        move = (move_x, move_y)
        if self.is_open(old_pos, move, board)[0]: # new_pos
            new_board = self.update_board(old_pos, new_pos, 0, board)

            #self.set_black_piece(old_pos, new_pos)

            if abs(move_x) % 2 == 0:
                middle_move = (move_x / 2, move_y / 2)
                middle_position_x = old_pos[0] + middle_move[0]
                middle_position_y = old_pos[1] + middle_move[1]
                middle_position = (middle_position_x, middle_position_y)
                new_board = self.remove_white_piece(middle_position, new_board)
                new_board = self.update_board(middle_position, middle_position, 1, new_board)
            return new_board
        else:
            raise ValueError('Invalid Move')
