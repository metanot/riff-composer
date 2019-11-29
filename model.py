from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import BatchNormalization
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Concatenate

def create_network(pitches, durations):
    """ create the structure of the neural network """
    # model = Sequential()
    # model.add(LSTM(
    #     512,
    #     input_shape=(network_input.shape[1], network_input.shape[2]),
    #     recurrent_dropout=0.3,
    #     return_sequences=True
    # ))
    # model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    # model.add(LSTM(512))
    # model.add(BatchNorm())
    # model.add(Dropout(0.3))
    # model.add(Dense(256))
    # model.add(Activation('relu'))
    # model.add(BatchNorm())
    # model.add(Dropout(0.3))
    # model.add(Dense(n_vocab))
    # model.add(Activation('softmax'))
    # model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # pitches = numpy.asarray(pitches, dtype=numpy.int)
    # durations = numpy.asarray(durations, dtype=numpy.int)

    pitch_input = Input(shape=(pitches.shape[1], pitches.shape[2]), name='pitch_in')
    duration_input = Input(shape=(durations.shape[1], durations.shape[2]), name='duration_in')
    sum_input = Concatenate()([pitch_input, duration_input])

    # function definitions
    lstm_function = LSTM(units=512, recurrent_dropout=0.3,return_sequences=True)(sum_input)
    lstm_function = LSTM(units=512, recurrent_dropout=0.3, return_sequences=True)(lstm_function)
    lstm_function = LSTM(units=512)(lstm_function)
    lstm_function = BatchNormalization()(lstm_function)
    lstm_function = Dropout(0.3)(lstm_function)
    lstm_function = Dense(256)(lstm_function)
    lstm_function = Activation('relu')(lstm_function)
    lstm_function = BatchNormalization()(lstm_function)
    lstm_function = Dropout(0.3)(lstm_function)

    pitch_function = Dense(pitches.shape[2], activation='softmax', name='pitch_out')
    duration_function = Dense(durations.shape[2], activation='softmax', name='duration_out')

    # function applications
    pitch_output = pitch_function(lstm_function)
    duration_output = duration_function(lstm_function)

    # model
    model = Model(inputs=[pitch_input, duration_input], outputs=[pitch_output, duration_output])
    model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], optimizer='RMSProp')

    return model