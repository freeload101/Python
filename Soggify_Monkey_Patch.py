#!/usr/bin/env python3
# Soggify Fixer :*(
# file format must be !
# {artist_name} - {track_num} - {album_name} - {track_name}.ogg
# {artist_name}/{album_name}{multi_disc_path}/{artist_name} - {track_num} - {album_name} - {track_name}.ogg 
# This script fixes Soggify meta data based on non standard Soggify settings!
# Recursively finds all .ogg files and processes them with 4 threads

import os
from pathlib import Path
from mutagen.oggvorbis import OggVorbis
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

print_lock = Lock()

def parse_filename(filename):
    """Parse filename to extract metadata components."""
    name = filename.replace('.ogg', '')
    parts = name.split(' - ')

    if len(parts) < 4:
        return None

    return {
        'artist': parts[0],
        'track_num': parts[1],
        'album': parts[2],
        'track_name': ' - '.join(parts[3:])
    }

def add_metadata_to_ogg(filepath):
    """Add metadata to OGG file based on filename."""
    try:
        metadata = parse_filename(os.path.basename(filepath))
        if not metadata:
            with print_lock:
                print(f"Could not parse filename: {filepath}")
            return False

        audio_file = OggVorbis(filepath)
        audio_file['ARTIST'] = metadata['artist']
        audio_file['ALBUM'] = metadata['album']
        audio_file['TITLE'] = metadata['track_name']
        audio_file['TRACKNUMBER'] = metadata['track_num']
        audio_file.save()

        with print_lock:
            print(f"Updated: {filepath}")
        return True

    except Exception as e:
        with print_lock:
            print(f"Error processing {filepath}: {str(e)}")
        return False

def find_and_process_ogg_files(root_path, max_workers=4):
    """Recursively find all OGG files and process them with thread pool."""
    root = Path(root_path)

    if not root.exists():
        print(f"Path does not exist: {root_path}")
        return

    # Find all .ogg files recursively, excluding hidden directories
    ogg_files = [f for f in root.rglob("*.ogg") if not any(part.startswith('.') for part in f.parts)]

    if not ogg_files:
        print("No OGG files found")
        return

    print(f"Found {len(ogg_files)} OGG files")
    print(f"Processing with {max_workers} threads...\n")

    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(add_metadata_to_ogg, str(ogg_file)): ogg_file for ogg_file in ogg_files}

        for future in as_completed(futures):
            if future.result():
                success_count += 1

    print(f"\nProcessed {success_count}/{len(ogg_files)} files successfully")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python Soggify_Monkey_Patch.py <root_directory>")
        sys.exit(1)

    find_and_process_ogg_files(sys.argv[1], max_workers=4)

