import glob
import json
from music21 import converter, instrument, note, chord

def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    notes = []

    for file in glob.glob("rammstein/*.mid*"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except:  # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        notes.extend(parse_notes(notes_to_parse))

    with open("data/notes.json", "w") as filepath:
        json.dump(notes, filepath)

    return notes


def parse_notes(notes_to_parse):
    notes = []

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(parse_note(element))
        elif isinstance(element, chord.Chord):
            notes.append(parse_chord(element))
        elif isinstance(element, note.Rest):
            notes.append(parse_rest(element))

    return notes


def parse_note(element):
    pitch = str(element.pitch)
    duration = element.duration.type
    return [pitch, duration]


def parse_chord(element):
    pitch = '.'.join(str(n.pitch) for n in element.notes)
    duration = element.duration.type
    return [pitch, duration]


def parse_rest(element):
    pitch = element.name
    duration = element.duration.type
    return [pitch, duration]