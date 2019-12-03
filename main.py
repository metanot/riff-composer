# Main entry point for riff-composer
# Place some midi files into midiFolder
# folder near this script and run:
# python main.py

import os
import configparser

from pathlib import Path
from packages.GetNotes import getNotes

# Setting variables and constants from config
confpath = Path('config.ini')
if not confpath.exists:
    createConfig(confpath)

config = configparser.ConfigParser()
config.read(confpath)
midiFolder = config.get("DEFAULT", "midiFolder")
jsonParsedDataDir = config.get("DEFAULT", "jsonParsedDataDir")

# Test configparser
print (midiFolder, jsonParsedDataDir)

# Test run for getNotes()
#getNotes(midiFolder)

