# name=Shift Handler
# url=https://github.com/TheNathanSpace/Launchkey-Mini-FL-Studio-Scale-Mode/
import time

import device
import midi
import transport

# Constants for message types
shift_DATA1 = 108
record_DATA1 = 117
play_DATA1 = 115
arrow_DATA1 = 104


def OnMidiMsg(event):
    """
    Handles MIDI note events, specifically the shift, play, and record button presses.

    :param event: The FlMidiMsg
    """
    event.handled = False

    # print("MIDI STATUS", event.midiId, "|", "MIDI DATA1", event.data1, "|",
    #       "MIDI DATA2", event.data2, "|", "MIDI status", event.status, "|",
    #       "Channel", (event.midiChan + 1), "| Sysex", event.sysex, "|", "Handled", event.handled)  # Prints MIDI data from pads, knobs and other buttons. Useful for debugging.

    if event.midiId == midi.MIDI_CONTROLCHANGE:
        if event.data1 == shift_DATA1:
            # Device 0 = port 170 = Note Handler
            if event.data2:
                device.dispatch(0, 0xF0, bytes([18]))
            else:
                device.dispatch(0, 0xF0, bytes([17]))
        elif event.data1 == record_DATA1:
            if event.data2:
                transport.record()
        elif event.data1 == play_DATA1:
            if event.data2:
                if transport.isPlaying():
                    transport.stop()
                else:
                    transport.start()
        elif event.data1 == arrow_DATA1:
            if event.data2:
                device.dispatch(0, 0xF0, bytes([20]))
            else:
                device.dispatch(0, 0xF0, bytes([19]))


def OnInit():
    print("Initialized shift handler\n")
    device.midiOutMsg(159, 16, 12, 127)
