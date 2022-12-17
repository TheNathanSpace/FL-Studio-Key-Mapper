major_scales = \
    """
    C	D	E	F	G	A	B
    G	A	B	C	D	E	F#
    D	E	F#	G	A	B	C#
    A	B	C#	D	E	F#	G#
    E	F#	G#	A	B	C#	D#
    B	C#	D#	E	F#	G#	A#
    F#	G#	A#	B	C#	D#	E#
    Db	Eb	F	Gb	Ab	Bb	C
    Ab	Bb	C	Db	Eb	F	G
    Eb	F	G	Ab	Bb	C	D
    Bb	C	D	Eb	F	G	A
    F	G	A	Bb	C	D	E
    """

minor_scales = \
    """
    A	B	C	D	E	F	G
    E	F#	G	A	B	C	D
    B	C#	D	E	F#	G	A
    F#	G#	A	B	C#	D	E
    C#	D#	E	F#	G#	A	B
    G#	A#	B	C#	D#	E	F#
    D#	E#	F#	G#	A#	B	C#
    A#	B#	C#	D#	E#	F#	G#
    D	E	F	G	A	Bb	C
    G	A	Bb	C	D	Eb	F
    C	D	Eb	F	G	Ab	Bb
    F	G	Ab	Bb	C	Db	Eb
    Bb	C	Db	Eb	F	Gb	Ab
    Eb	F	Gb	Ab	Bb	Cb	Db
    Ab	Bb	Cb	Db	Eb	Fb	Gb
    """

all_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

sharps_flats_map = {
    "F#": "Gb",
    "C#": "Db",
    "G#": "Ab",
    "D#": "Eb",
    "A#": "Bb",
    "E#": "F",
}

flats_sharps_map = {v: k for k, v in sharps_flats_map.items()}
