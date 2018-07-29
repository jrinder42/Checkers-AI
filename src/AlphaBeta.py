from copy import deepcopy
import cPickle

from Board import Actions

class AlphaBeta(Actions):

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

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.game_over(board):
            return self.evaluate(board)

        if maximizingPlayer:
            v = float('-inf')
            moves = self.generate_black_moves(board)
            self.BEST_MOVE = moves[0]
            for move in moves:
                child = deepcopy(board)
                self.move_black(child, *move)
                best_value = self.alphabeta(child, depth - 1, alpha, beta, False)
                if best_value > v:
                    v = best_value
                    self.BEST_MOVE = move
                alpha = max(alpha, v)
                if beta <= alpha: # (* beta cut-off *)
                    break
            return v

        else:
            v = float('inf')
            moves = self.generate_white_moves(board)
            self.BEST_MOVE = moves[0]
            for move in moves:
                child = deepcopy(board)
                self.move_white(child, *move)
                best_value = self.alphabeta(child, depth - 1, alpha, beta, True)
                if best_value < v:
                    v = best_value
                    self.BEST_MOVE = move
                beta = min(beta, v)
                if beta <= alpha: # (* alpha cut-off *)
                    break
            return v

    def evaluate(self, board): # for AI
        # sum(my pieces) - sum(oponent pieces)
        return len(self.get_black_pieces(board)) - len(self.get_white_pieces(board))



