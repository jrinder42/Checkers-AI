from copy import deepcopy
import cPickle

from Board import Actions



class Negamax_AB(Actions):

    BEST_MOVE = None

    def __init__(self):
        Actions.__init__(self)

    def __deepcopy__(self, memodict={}): # faster than built-in
        g = cPickle.loads(cPickle.dumps(self, -1))
        return g

    def game_over(self, board):
        white_pieces = self.get_white_pieces(board)
        black_pieces = self.get_black_pieces(board)
        if not white_pieces:
            print "Black has won"
            return True
        elif not black_pieces:
            print "White has won"
            return True
        return False

    def negamax(self, board, depth, alpha, beta, color):
        if depth <= 0 or self.game_over(board):
            return color * self.evaluate(board)

        moves = self.generate_black_moves(board)
        for move in moves:
            child = deepcopy(board)
            self.move_black(child, *move)
            score = -self.negamax(child, depth - 1, -beta, -alpha, -color)
            if score >= alpha:
                alpha = score
                self.BEST_MOVE = move
            if alpha >= beta:
                break
        return alpha

    def evaluate(self, board): # for AI
        # sum(my pieces) - sum(oponent pieces)
        return len(self.get_black_pieces(board)) - len(self.get_white_pieces(board))



class Negamax(Actions):

    BEST_MOVE = None

    def __init__(self):
        Actions.__init__(self)

    def __deepcopy__(self, memodict={}): # faster than built-in
        g = cPickle.loads(cPickle.dumps(self, -1))
        return g

    def game_over(self, board):
        white_pieces = self.get_white_pieces(board)
        black_pieces = self.get_black_pieces(board)
        if not white_pieces:
            print "Black has won"
            return True
        elif not black_pieces:
            print "White has won"
            return True
        return False

    def negamax(self, board, depth, color):
        if depth == 0 or self.game_over(board):
            return color * self.evaluate(board)

        v = float('-inf')
        moves = self.generate_black_moves(board)
        self.BEST_MOVE = moves[0]
        for move in moves:
            child = deepcopy(board)
            self.move_black(child, *move)
            v = max(v, -self.negamax(child, depth - 1, -color))
            self.BEST_MOVE = move
        return v

    def evaluate(self, board): # for AI
        # sum(my pieces) - sum(oponent pieces)
        return len(self.get_black_pieces(board)) - len(self.get_white_pieces(board))



