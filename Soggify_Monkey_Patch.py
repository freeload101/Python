#!/usr/bin/env python3
# Soggify Fixer :*(
# file format must be !
# {artist_name} - {track_num} - {album_name} - {track_name}.ogg
# {artist_name}/{album_name}{multi_disc_path}/{artist_name} - {track_num} - {album_name} - {track_name}.ogg 
# This script fixes Soggify meta data based on non standard Soggify settings!
# find . -not -path "*/.*" -type d -exec python Soggify_Monkey_Patch.py '{}' \;


import os
import re
from pathlib import Path
from mutagen.oggvorbis import OggVorbis
from mutagen import File

def parse_filename(filename):
    """Parse filename to extract metadata components."""
    # Remove .ogg extension
    name = filename.replace('.ogg', '')

    # Split by ' - ' to get components
    parts = name.split(' - ')

    if len(parts) < 4:
        return None

    artist = parts[0]
    track_num = parts[1]
    album = parts[2]
    # Join remaining parts as track name (handles tracks with ' - ' in title)
    track_name = ' - '.join(parts[3:])

    return {
        'artist': artist,
        'track_num': track_num,
        'album': album,
        'track_name': track_name
    }

def add_metadata_to_ogg(filepath):
    """Add metadata to OGG file based on filename."""
    try:
        # Parse filename
        metadata = parse_filename(os.path.basename(filepath))
        if not metadata:
            print(f"Could not parse filename: {filepath}")
            return False

        # Load OGG file
        audio_file = OggVorbis(filepath)

        # Add metadata
        audio_file['ARTIST'] = metadata['artist']
        audio_file['ALBUM'] = metadata['album']
        audio_file['TITLE'] = metadata['track_name']
        audio_file['TRACKNUMBER'] = metadata['track_num']

        # Save changes
        audio_file.save()
        print(f"Updated: {os.path.basename(filepath)}")
        return True

    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

def process_directory(directory_path):
    """Process all OGG files in directory."""
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Directory does not exist: {directory_path}")
        return

    ogg_files = list(directory.glob("*.ogg"))

    if not ogg_files:
        print("No OGG files found in directory")
        return

    print(f"Found {len(ogg_files)} OGG files")

    success_count = 0
    for ogg_file in ogg_files:
        if add_metadata_to_ogg(str(ogg_file)):
            success_count += 1

    print(f"\nProcessed {success_count}/{len(ogg_files)} files successfully")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ogg_metadata.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    process_directory(directory_path)

