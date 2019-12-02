# Main entry point for riff-composer
# Place some midi files into midiFolder
# folder near this script and run:
# python main.py

import os
from pathlib import Path
from packages.GetNotes import getNotes

baseDir = Path(__file__).resolve().parent
midiFolder = baseDir.joinpath('midiFolder/')
rawParsedDataDir = baseDir.joinpath('rawParsedData/')
print ("main: Setting data directories:")
print (f"    main: Setting midi directory to {midiFolder}")
print (f"    main: Setting raw parsed data directory to {rawParsedDataDir}")


# Test run for getNotes()
getNotes(midiFolder, rawParsedDataDir)

