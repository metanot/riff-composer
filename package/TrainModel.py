from get_notes import get_notes
from model import create_network

import pandas as pd
import numpy
import json

from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint


def train_network():
    notes = get_notes()

    with open("data/notes.json", "w") as filename:
        json.dump(notes, filename)

    notes_df = pd.DataFrame(notes, columns=['pitch', 'duration'])

    pitches = notes_df['pitch']
    durations = notes_df['duration']

    pitch_vocab = sorted(set(item for item in pitches))
    duration_vocab = sorted(set(item for item in durations))

    with open("data/pitch_vocab.json", "w") as filename:
        json.dump(pitch_vocab, filename)

    with open("data/duration_vocab.json", "w") as filename:
        json.dump(duration_vocab, filename)

    # print("notes_df:")
    # print(notes_df)

    look_back = 4

    in_pitches, in_durations, out_pitches, out_durations = prepare_sequences(notes_df, look_back)

    model = create_network(timesteps=look_back,
                           pitch_vocab_size=len(pitch_vocab),
                           duration_vocab_size=len(duration_vocab))
    model.summary()

    train(model, in_pitches, in_durations, out_pitches, out_durations)


def prepare_sequences(notes, look_back):
    pitches = notes['pitch']
    durations = notes['duration']

    pitch_vocab = sorted(set(item for item in pitches))
    duration_vocab = sorted(set(item for item in durations))

    print("pitch_vocab:")
    print(pitch_vocab)

    print("duration_vocab:")
    print(duration_vocab)

    pitch_to_int = dict((note, number) for number, note in enumerate(pitch_vocab))
    duration_to_int = dict((note, number) for number, note in enumerate(duration_vocab))

    pitches_in = []
    durations_in = []

    pitches_out = []
    durations_out = []

    for i in range(notes.shape[0] - look_back):
        pitch_sequence_in = pitches[i:(i + look_back)]
        pitch_sequence_out = pitches[i + look_back]

        duration_sequence_in = durations[i:(i + look_back)]
        duration_sequence_out = durations[i + look_back]

        pitches_in.append([pitch_to_int[char] for char in pitch_sequence_in])
        pitches_out.append(pitch_to_int[pitch_sequence_out])

        durations_in.append([duration_to_int[char] for char in duration_sequence_in])
        durations_out.append(duration_to_int[duration_sequence_out])

    pitches_in = numpy.array(pitches_in)
    durations_in = numpy.array(durations_in)
    pitches_out = numpy.array(pitches_out)
    durations_out = numpy.array(durations_out)

    pitches_in = np_utils.to_categorical(pitches_in)
    durations_in = np_utils.to_categorical(durations_in)
    pitches_out = np_utils.to_categorical(pitches_out)
    durations_out = np_utils.to_categorical(durations_out)

    # print('\npitches_in:')
    # print(pitches_in)
    #
    # print('\npitches_out:')
    # print(pitches_out)
    #
    # print('\ndurations_in:')
    # print(durations_in)
    #
    # print('\ndurations_out:')
    # print(durations_out)

    return (pitches_in, durations_in, pitches_out, durations_out)


def train(model, pitch_in, duration_in, pitch_out, duration_out):
    """ train the neural network """
    filepath = "weights/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit([pitch_in, duration_in], [pitch_out, duration_out], epochs=20, batch_size=16, callbacks=callbacks_list)


if __name__ == '__main__':
    train_network()
