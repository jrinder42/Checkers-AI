# Principal Variation Search (PVS)

from copy import deepcopy
import cPickle

from Board import Actions

class Negascout(Actions):

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

    def pvs(self, board, depth, alpha, beta, color):
        if depth <= 0 or self.game_over(board):
            return color * self.evaluate(board)

        moves = self.generate_black_moves(board)
        for move in moves:
            child = deepcopy(board)
            self.move_black(child, *move)
            if move == moves[0]:
                score = -self.pvs(child, depth - 1, -beta, -alpha, -color)
            else:
                score = -self.pvs(child, depth - 1, -alpha - 1, -alpha, -color) # search with a null window
                if alpha < score and score < beta: # if it failed high
                    score = -self.pvs(child, depth - 1, -beta, -score, -color) # do a full re-search
            if score >= alpha:
                alpha = score
                self.BEST_MOVE = move
            if alpha >= beta:
                break # beta cut-off
        return alpha

    def evaluate(self, board): # for AI
        # sum(my pieces) - sum(oponent pieces)
        return len(self.get_black_pieces(board)) - len(self.get_white_pieces(board))


