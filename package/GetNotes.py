# Functions for converting raw midi files
# to input data for neural network

import pathlib
import glob
from music21 import converter, instrument, note, chord

# Getting notes for parsing
def getNotes(midiFiles):
    notes = []

    for file in midiFiles.absolute().glob('*.mid'):
        print("Parsing %s" % file)
        midi = converter.parse(file)
        notesToParse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notesToParse = s2.parts[0].recurse()
        except:  # file has notes in a flat structure
            notesToParse = midi.flat.notes
        notes.extend(parseNotes(notesToParse))
    return notes

# Parsing notes to input data according with single notes, chords, or something else
def parseNotes(notesToParse):
    notes = []

    for element in notesToParse:
        if isinstance(element, note.Note):
            notes.append(parseNote(element))
        elif isinstance(element, chord.Chord):
            notes.append(parseChord(element))
        elif isinstance(element, note.Rest):
            notes.append(parseRest(element))
    return notes

# Single-note parsing for parseNotes()
def parseNote(element):
    pitch = str(element.pitch)
    duration = element.duration.type
    return [pitch, duration]

# Chord parsing for parseNotes()
def parseChord(element):
    pitch = '.'.join(str(n.pitch) for n in element.notes)
    duration = element.duration.type
    return [pitch, duration]

# Other miscellaneous parsing for parseNotes()
def parseRest(element):
    pitch = element.name
    duration = element.duration.type
    return [pitch, duration]
