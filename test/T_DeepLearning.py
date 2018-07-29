# Testing DeepLearning Algorithm

from DeepLearning import QLearning

import numpy as np
from keras.optimizers import RMSprop
from keras.models import model_from_json

def test(learning_rate=0.001):
    'currently no error checking for valid user moves'

    ML = QLearning()
    board = ML.init_board()

    # load json and create model
    json_file = open("checkers_model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json) # loaded_model
    # load weights into new model
    model.load_weights("checkers_model.h5") # loaded_model
    rms = RMSprop(lr=learning_rate)
    model.compile(loss='mse', optimizer=rms) # compile model
    print("Loaded model from disk")

    player = True
    while not ML.game_over(board):
        if player: # black - AI
            print ML.generate_black_moves(board)
            potential_moves = ML.generate_black_moves(board)
            qval = list(model.predict(np.array(board).reshape(1, 64), batch_size=1)[0])
            future_moves = [moves[1] for moves in potential_moves] # future piece position
            flat_qval = [qval[j] for j in xrange(64) if (j / 8, j % 8) in future_moves]
            action = np.argmax(flat_qval)
            move = potential_moves[action]
            board = ML.move_black(board, *move)
            ML.print_board(board)
            player = False
        else:
            print ML.generate_white_moves(board)
            i = int(raw_input("Enter piece i: "))
            j = int(raw_input("Enter piece j: "))
            i_new = int(raw_input("Enter new i: "))
            j_new = int(raw_input("Enter new j: "))
            board = ML.move_white(board, (i, j), (i_new, j_new))
            ML.print_board(board)
            player = True


if __name__ == '__main__':

    test()