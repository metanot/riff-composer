# Main entry point for riff-composer
# Place some midi files into midiFolder
# folder near this script and run:
# python main.py

import os
from pathlib import Path
from packages.GetNotes import getNotes

midiBaseDir = Path(__file__).resolve().parent
midiFolder = midiBaseDir.joinpath('midiFolder/')

print (f"main: Setting midiFolder variable to {midiFolder}")

# Test run for getNotes()
getNotes(midiFolder)

