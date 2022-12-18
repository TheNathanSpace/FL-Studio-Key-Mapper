# name=Note Handler
# receiveFrom=Shift Handler
# url=https://github.com/TheNathanSpace/Launchkey-Mini-FL-Studio-Scale-Mode/
import device
import midi
import ui

import constants

major_scales_dict = {}
minor_scales_dict = {}

id_to_name_dict = {}
name_to_id_dict = {}

shift_is_on = False
arrow_is_on = False
is_minor = False

current_key = "C"


def index_of(list_in, item):
    """
    Returns the index of an item in a list.

    :param list_in: The list to traverse.
    :param item: The item to find in the list.
    :return: The index of the first occurrence of the item, or -1 if not found.
    """
    counter = 0
    for i in list_in:
        if item == i:
            return counter
        counter += 1
    return -1


def read_scales_file(scale_string):
    """
    Parses a string of scales into a dictionary.

    :param scale_string: A string of scales. Each line contains a scale, starting at the root note and
                        ending before the next root note (so there are 7 notes). Spaces and blank
                        newlines are ignored.
    :return: A dictionary mapping the root note to a list of notes for each scale.
    """
    loc_scales_dict = {}
    lines = scale_string.split("\n")
    for line in lines:
        # Skip comments and blank lines
        if line == "\n":
            continue

        line = line.replace(" ", "")
        split_line = line.split("\t")
        root_note = split_line[0]
        loc_scales_dict[root_note] = []
        for note in split_line:
            note = note.replace("\n", "")
            loc_scales_dict[root_note].append(note)

    return loc_scales_dict


def map_note_ids(all_notes):
    """
    Creates a dictionary mapping note IDs from 0-127 to note names from C0 to C10

    :param all_notes: A list of all possible note names, from C to B
    :return: A dictionary mapping note IDs (int) --> note names including octave (str)
    """
    loc_id_to_name_dict = {}
    note_index = 0
    octave = 0
    for i in range(0, 128):
        note_letter = all_notes[note_index]
        loc_id_to_name_dict[i] = note_letter + str(octave)

        note_index += 1
        if note_index == 12:
            note_index = 0

        if all_notes[note_index] == "C":
            octave += 1

    return loc_id_to_name_dict


def get_no_octave(note_id):
    """
    Returns the name of a note without the octave.

    :param note_id: The ID of the note, as an int from 0-127
    :return: The name of the note, from A-G, including # or b as relevant
    """

    no_octave = ''.join([i for i in id_to_name_dict[note_id] if not i.isdigit()])
    return no_octave


def get_c_index(note_id):
    """
    Returns the index of a note in the key of C.

    :param note_id: The ID of the note, as an int from 0-127
    :return: The index of the note, as an int from 0-6
    """

    return index_of(major_scales_dict["C"], get_no_octave(note_id))


def get_octave(note_id):
    """
    Returns the octave of a note, from 0-10.

    :param note_id: The ID of the note, as an int from 0-127
    :return: The octave of the note, as an int from 0-10
    """

    just_octave = ''.join([i for i in id_to_name_dict[note_id] if i.isdigit()])
    return just_octave


def OnMidiMsg(event):
    """
    Handles MIDI note events.

    :param event: The FlMidiMsg
    """
    event.handled = False

    print("MIDI STATUS", event.midiId, "|", "MIDI DATA1", event.data1, "|",
          "MIDI DATA2", event.data2, "|", "MIDI status", event.status, "|",
          "Channel", (event.midiChan + 1), "| Sysex", event.sysex, "|", "Handled", event.handled)  # Prints MIDI data from pads, knobs and other buttons. Useful for debugging.

    if event.midiId == midi.MIDI_NOTEON:
        if event.pmeFlags & midi.PME_System != 0:
            # print("\nBefore: " + id_to_name_dict[event.data1] + " on channel " + str(event.midiChan))
            global current_key
            global is_minor

            # Only perform this on key down, not up
            if shift_is_on and event.data2 != 0:
                change_to = get_no_octave(event.data1)

                # Decide if major or minor key
                if arrow_is_on:
                    major_minor = " minor"
                    scales_dict = minor_scales_dict
                    is_minor = True
                else:
                    major_minor = " major"
                    scales_dict = major_scales_dict
                    is_minor = False

                # Parse key to change to
                if change_to not in scales_dict:
                    # Convert sharp to flat
                    change_to = constants.sharps_flats_map[change_to]

                    if change_to not in scales_dict:
                        message = "Couldn't change key signature to " + change_to + major_minor
                        ui.setHintMsg(message)
                        print(message)
                        return

                current_key = change_to
                message = "Changed mapped key signature to: " + current_key + major_minor
                ui.setHintMsg(message)
                print(message)
                event.handled = True
                return

            if current_key != "C" and event.midiChan == 0:
                # Ignore sharps/flats while key is mapped
                if "#" in id_to_name_dict[event.data1] or "b" in id_to_name_dict[event.data1]:
                    event.handled = True
                    return

                # Get position of original note in scale
                c_index = get_c_index(event.data1)

                # Choose if major/minor
                if is_minor:
                    scales_dict = minor_scales_dict
                else:
                    scales_dict = major_scales_dict

                # Get translated note from new key
                translated_key = scales_dict[current_key][c_index]
                octave = get_octave(event.data1)

                # Fix octave if note is late enough
                for note in scales_dict[current_key][:c_index + 1]:
                    if "C" in note:
                        octave = int(octave) + 1
                        octave = str(octave)
                        break

                # Get note ID
                translated_key_with_octave = translated_key + octave
                if translated_key_with_octave in name_to_id_dict:
                    translated_id = name_to_id_dict[translated_key_with_octave]
                else:
                    # Convert flat to sharp if necessary
                    translated_id = name_to_id_dict[constants.flats_sharps_map[translated_key] + octave]

                # Modify event note
                event.data1 = translated_id
                # print("After: " + id_to_name_dict[event.data1] + " on channel " + str(event.midiChan))


def OnSysEx(event):
    """
    Handles SysEx events. The only expected events are shift on/off
    and arrow on/off, sent by the Shift handler.

    :param event: The SysexMidiMsg
    """
    received_message = int.from_bytes(bytes = event.sysex, byteorder = 'big')

    global shift_is_on
    global arrow_is_on
    if received_message == 18:
        shift_is_on = True
    elif received_message == 17:
        shift_is_on = False
    elif received_message == 20:
        arrow_is_on = True
    elif received_message == 19:
        arrow_is_on = False


def OnInit():
    # Create scale dicts
    global major_scales_dict
    global minor_scales_dict
    major_scales_dict = read_scales_file(constants.major_scales)
    minor_scales_dict = read_scales_file(constants.minor_scales)

    # Create id/name maps (both directions)
    global id_to_name_dict
    global name_to_id_dict
    id_to_name_dict = map_note_ids(constants.all_notes)
    name_to_id_dict = {v: k for k, v in id_to_name_dict.items()}

    print("Initialized note handler\n")
