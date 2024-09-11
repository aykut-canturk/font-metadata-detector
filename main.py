from fontTools.ttLib import TTFont

# Load the font file
FONT_PATH = (
    "c3e0142c-3a7e-4be9-bf72-7e183460f273.woff"  # Replace with your font file path
)
font = TTFont(FONT_PATH)


# Extracting font metadata
def _get_font_metadata(font):
    metadata = {}

    # Get the 'name' table which stores various metadata about the font
    name_table = font["name"]

    for record in name_table.names:
        name = record.nameID
        value = record.string
        try:
            # Decode name records if necessary
            if b"\000" in value:
                value = value.decode("utf-16-be")
            else:
                value = value.decode("utf-8")
        except UnicodeDecodeError:
            value = value.decode("latin1")

        # Store the decoded values in the dictionary
        metadata[name] = value

    return metadata


def _write_to_file(metadata):
    with open("font_metadata.txt", "w", encoding="utf-8") as f:
        for name_id, val in metadata.items():
            f.write(f"NameID {name_id}: {val}\n")


meta = _get_font_metadata(font)
_write_to_file(meta)
# for name_id, val in meta.items():
#     print(f"NameID {name_id}: {val}")
