import json
from pathlib import Path

input_file = Path("keys.txt")
if not input_file.exists():
    raise FileNotFoundError

with open(file = input_file, mode = "r", encoding = "utf-8") as opened:
    scale_dict = {}
    lines = opened.readlines()
    for line in lines:
        # Skip comments and blank lines
        if "#" in line:
            continue
        if line == "\n":
            continue

        split_line = line.split("\t")
        root_note = split_line[0]
        scale_dict[root_note] = []
        for note in split_line[1:]:
            note = note.replace("\n", "")
            scale_dict[root_note].append(note)

output_file = Path("scale_dict.json")
output_file.touch(exist_ok = True)
output_file.write_text(json.dumps(scale_dict, indent = 4, ensure_ascii = False), encoding = "utf-8")
