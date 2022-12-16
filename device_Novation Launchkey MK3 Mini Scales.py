# name=Novation Launckey MK3 Mini Scales
# url=https://forum.image-line.com/viewtopic.php?p=1483607#p1483607

# This import section is loading the back-end code required to execute the script. You may not need all modules that are available for all scripts.
import json
from pathlib import Path
from typing import List

import midi

# 48 = C4
# 60 = C5
# 72 = C6
from fl_classes import FlMidiMsg

flat = "♭"
sharp = "♯"

scales_dict = None

c_scale = ["C", "D", "E", "F", "G", "A", "B"]


def index_of(list_in: List, item):
    counter = 0
    for i in list_in:
        if item == i:
            return counter
        counter += 1
    return -1


def read_scales_file():
    scales_file = Path("scale_dict.json")
    if not scales_file.exists():
        raise FileNotFoundError("scale_dict.json file not found! Generate it using process_scales.py and keys.txt.")

    global scales_dict
    scales_dict = json.loads(scales_file.read_text(encoding = "utf-8"))


class MidiHandler:

    def OnMidiMsg(self, event: FlMidiMsg):
        event.handled = True
        if event.midiId == midi.MIDI_NOTEON:
            if event.pmeFlags & midi.PME_System != 0:

                print(event.data1, event.data2)

            else:
                event.handled = False
        else:
            event.handled = False


Simple = MidiHandler()


def OnMidiMsg(event):
    Simple.OnMidiMsg(event)
