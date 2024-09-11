# usage: python main.py [-h] [--save_to_file SAVE_TO_FILE] font_path

import os
import argparse
from fontTools.ttLib import TTFont


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
    print("Writing metadata to file")
    with open("font_metadata.txt", "w", encoding="utf-8") as f:
        for name_id, val in metadata.items():
            f.write(f"NameID {name_id}: {val}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font_path", help="Path to font file")
    parser.add_argument(
        "--save_to_file",
        type=int,
        default=False,
        help="Save the metadata to a file",
    )

    args = parser.parse_args()

    if not args.font_path:
        print("Please provide a path to the font file")
        return

    if not os.path.exists(args.font_path):
        print("Font file does not exist")
        return

    font_path = args.font_path
    save_to_file = args.save_to_file

    print("save_to_file: ", save_to_file)

    font = TTFont(font_path)
    metadata = _get_font_metadata(font)
    print(metadata)

    if save_to_file == 1:
        _write_to_file(metadata)

    print("Font metadata extracted successfully")


if __name__ == "__main__":
    main()
