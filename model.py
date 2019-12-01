from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import BatchNormalization
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Concatenate

def create_network(timesteps, pitch_vocab_size, duration_vocab_size):
    pitch_input = Input(shape=(timesteps, pitch_vocab_size), name='pitch_in')
    duration_input = Input(shape=(timesteps, duration_vocab_size), name='duration_in')
    sum_input = Concatenate()([pitch_input, duration_input])

    # function definitions
    lstm_function = LSTM(units=512, recurrent_dropout=0.3, return_sequences=True)(sum_input)
    lstm_function = LSTM(units=512, recurrent_dropout=0.3, return_sequences=True)(lstm_function)
    lstm_function = LSTM(units=512)(lstm_function)
    lstm_function = BatchNormalization()(lstm_function)
    lstm_function = Dropout(0.3)(lstm_function)
    lstm_function = Dense(256)(lstm_function)
    lstm_function = Activation('relu')(lstm_function)
    lstm_function = BatchNormalization()(lstm_function)
    lstm_function = Dropout(0.3)(lstm_function)

    pitch_function = Dense(pitch_vocab_size, activation='softmax', name='pitch_out')
    duration_function = Dense(duration_vocab_size, activation='softmax', name='duration_out')

    # function applications
    pitch_output = pitch_function(lstm_function)
    duration_output = duration_function(lstm_function)

    # model
    model = Model(inputs=[pitch_input, duration_input], outputs=[pitch_output, duration_output])
    model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], optimizer='RMSProp')

    return model