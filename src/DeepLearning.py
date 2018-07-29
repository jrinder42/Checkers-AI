from copy import deepcopy
import cPickle

from Board import Actions

import numpy as np
import os
import random
from collections import deque
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.models import model_from_json
# A neural network will not work! - not continuous problem (simulated annealing) / MCTS with alpha-beta pruning

class QLearning(Actions):

    def __init__(self):
        Actions.__init__(self)
        self.buffer = 10000
        self.replay = deque(maxlen=self.buffer)
        self.h = 0
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.bs = 32 # batch size - between 32 and 512 On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima
        # Keskar, Mudigere, Nocedal, Tak, Peter Tang, etc.


    def __deepcopy__(self, memodict={}):
        g = cPickle.loads(cPickle.dumps(self, -1))
        return g


    def game_over(self, board): # don't use function
        white_pieces = self.get_white_pieces(board)
        black_pieces = self.get_black_pieces(board)
        if len(white_pieces) == 0 and len(black_pieces) > 0:
            print "Black has won"
            return True
        elif len(black_pieces) == 0 and len(white_pieces) > 0:
            print "White has won"
            return True
        return False


    def get_reward(self, board, game_length): # once per game
        # game length to 100 moves
        # old_state
        # new_state
        white = self.get_white_pieces(board)
        black = self.get_black_pieces(board)

        if len(white) == 0:
            return 100
        elif len(black) == 0:
            return -100
        return len(black) - len(white)

    def _build_model(self):
        model = Sequential()
        model.add(Dense(32, kernel_initializer='lecun_uniform', input_shape=(64, )))
        model.add(Activation('relu')) #42
        #model.add(Dropout(0.2))

        model.add(Dense(32, kernel_initializer='lecun_uniform'))
        model.add(Activation('relu')) #28
        #model.add(Dropout(0.2))

        model.add(Dense(64, kernel_initializer='lecun_uniform'))
        model.add(Activation('tanh'))

        rms = RMSprop(lr=self.learning_rate)
        model.compile(loss='mse', optimizer=rms)

        return model

    def train_model(self):
        # load model
        # 450
        # Count: 2205000 games

        if os.path.isfile("checkers_model.json") and os.path.isfile("checkers_model.h5") \
           and os.path.isfile("checkers_h.txt") and os.path.isfile("checkers_replay.txt"):
            self.epsilon = 0.1
            # load json and create model
            json_file = open("checkers_model.json", "r")
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json) # loaded_model
            # load weights into new model
            model.load_weights("checkers_model.h5") # loaded_model
            rms = RMSprop(lr=self.learning_rate)
            model.compile(loss='mse', optimizer=rms) # compile model
            print("Loaded model from disk")

            with open("checkers_h.txt", "rb") as json_data:
                self.h = cPickle.load(json_data)
            with open("checkers_replay.txt", "rb") as json_data:
                self.replay = cPickle.load(json_data)
        else:
            model = self._build_model()

        print 'Length of replay:', len(self.replay)
        print 'Value of h:', self.h

        epochs = 10000

        win = 0
        lose = 0
        tie = 0

        for i in xrange(epochs):
            state = self.init_board()
            X_train = []
            y_train = []
            minibatch = []
            game_length = 0
            previous_h = self.h
            previous_replay = self.replay
            while game_length <= 1000 and not self.game_over(state): # sometimes the game gets stuck
                potential_moves = self.generate_black_moves(state)
                if len(potential_moves) == 0: # if no black moves available
                    potential_white_moves = self.generate_white_moves(state)
                    if len(potential_white_moves) == 0: # if no white moves available -- end
                        print "What has happened?"
                        break
                    white_move = random.sample(potential_white_moves, 1)
                    state = self.move_white(state, *white_move[0])
                    game_length += 1
                    continue
                qval = list(model.predict(np.array(state).reshape(1, 64), batch_size=1)[0])
                future_moves = [moves[1] for moves in potential_moves] # future piece position
                #present_moves = [moves[0] for moves in potential_moves] # current piece position
                flat_qval = [qval[j] for j in xrange(64) if (j / 8, j % 8) in future_moves]
                if random.random() < self.epsilon:
                    action = np.random.randint(0, len(potential_moves)) # index
                else:
                    action = np.argmax(flat_qval) # check for multiple occurances of same value
                move = potential_moves[action]
                s = deepcopy(state)
                new_state = self.move_black(s, *move)

                reward = self.get_reward(new_state, game_length)


                # make move - more advanced AI
                #self.alphabeta(self, 3, float('-inf'), float('inf'), False)
                #white_move = self.BEST_MOVE
                potential_white_moves = self.generate_white_moves(new_state)
                if len(potential_white_moves) > 0:
                    white_move = random.sample(potential_white_moves, 1)# make random move
                    new_state = self.move_white(new_state, *white_move[0])

                if len(self.replay) < self.buffer:
                    self.replay.append((state, action, reward, new_state))
                else:
                    if self.h < self.buffer - 1:
                        self.h += 1
                    else:
                        self.h = 0
                    self.replay[self.h] = (state, action, reward, new_state)
                    minibatch = random.sample(self.replay, self.bs)
                    X_train = []
                    y_train = []
                game_length += 1
                state = new_state
            if len(self.replay) >= self.buffer and game_length < 1000:
                for memory in minibatch:
                    old_state, action, reward, new_state = memory
                    old_qval = model.predict(np.array(old_state).reshape(1, 64), batch_size=1)[0] #list?
                    newQ = model.predict(np.array(new_state).reshape(1, 64), batch_size=1)[0] #new_qval

                    if not old_qval.size and not newQ.size: # if either piece cannot make a move
                        continue

                    #maxQ = np.max(newQ) # should prune
                    '''
                    move_set = self.generate_black_moves(new_state)
                    if len(move_set) == 0:
                        maxQ = 0
                    else: # takes a long time
                        newQ = list(newQ)
                        new_moves = [moves[0][0] * 8 + moves[0][1] for moves in move_set]
                        maxQ = max([newQ[j] for j in new_moves])
                    '''
                    move_set = self.get_black_pieces(new_state)
                    new_black_moves = [moves[0] * 8 + moves[1] for moves in move_set]
                    if len(new_black_moves) == 0:
                        maxQ = 0
                    else:
                        maxQ = np.max([newQ[j] for j in new_black_moves])

                    y = np.zeros((1, len(old_qval)))
                    y[:] = old_qval[:] # y = deepcopy(old_qval)
                    #if reward == -1:
                    if abs(reward) != 100:
                        update = reward + self.gamma * maxQ
                    else:
                        update = reward

                    y[0, action] = update
                    X_train.append(np.array(old_state).reshape(64, ))
                    y_train.append(y.reshape(len(old_qval), ))

                X_train = np.array(X_train)
                y_train = np.array(y_train)
                model.fit(X_train, y_train, batch_size=self.bs, epochs=1, verbose=1)



            print "Episode #: %s" % (i, )

            signal = -1
            if game_length >= 1000:
                white_kings = 0
                black_kings = 0
                white_pieces = 0
                black_pieces = 0
                for piece in self.get_white_pieces(state):
                    if self.is_king(piece, 0, state):
                        white_kings += 1
                    else:
                        white_pieces += 1
                for piece in self.get_black_pieces(state):
                    if self.is_king(piece, 1, state):
                        black_kings += 1
                    else:
                        black_pieces += 1
                if (black_pieces + black_kings) - (white_pieces + white_kings) > 0:# black was winning
                    signal = 1
                elif (black_pieces + black_kings) - (white_pieces + white_kings) < 0: # white was winning
                    signal = 0
                else: # nobody could have moved
                    signal = 2


            if (len(self.get_white_pieces(state)) > 0 and len(self.get_black_pieces(state)) == 0) or signal == 0:
                print "White Won"
                lose += 1
            elif (len(self.get_black_pieces(state)) > 0 and len(self.get_white_pieces(state)) == 0) or signal == 1:
                print "Black Won"
                win += 1
            elif signal != 2:
                print "Game Ended Early"
                tie += 1
                self.h = previous_h
                self.replay = previous_replay

            print "## ------------------------------------- RESULTS ------------------------------------- ##"
            print "Win: %d       Lose: %d        Tie: %d         Epsilon: %f        Win Rate: %f" \
                         % (win, lose, tie, self.epsilon, float(win)/(lose + win))

            if self.epsilon > self.epsilon_min:
                #self.epsilon -= 1. / epochs #- slower than below
                self.epsilon *= self.epsilon_decay


        # Save model
        model_json = model.to_json()
        with open("checkers_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("checkers_model.h5")
        print("Saved checkers_model to disk")

        with open("checkers_h.txt", "wb") as json_file:
            cPickle.dump(self.h, json_file)
        with open("checkers_replay.txt", "wb") as json_file:
            cPickle.dump(self.replay, json_file)


if __name__ == '__main__':

    checkers = QLearning()
    checkers.train_model()