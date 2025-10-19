"""
This script explores a gigantic json file contained inside a galaxy.json.gz file and prints out the first 10 entries
without loading the entire file into memory.
"""

import json
import gzip
import datetime
import os
from typing import Dict, List


def get_duration(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    duration = end_time - start_time
    # Format duration as a string hh:mm:ss
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def read_first_n_entries(file_path: str, n: int = 10) -> List[Dict]:
    """
    Reads the first n entries from a gzipped JSON file without loading the entire file into memory.
    Assumes the JSON file contains an array of objects.
    """
    entries = []

    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        # Skip the opening bracket
        f.read(1)  # Read '['

        # Read entries one by one
        buffer = ""
        bracket_count = 0
        in_string = False
        escape_next = False

        while len(entries) < n:
            char = f.read(1)
            if not char:  # End of file
                break

            buffer += char

            # Handle string literals (to ignore brackets inside strings)
            if escape_next:
                escape_next = False
                continue

            if char == "\\":
                escape_next = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            # Count brackets to find complete objects
            if char == "{":
                bracket_count += 1
            elif char == "}":
                bracket_count -= 1

                # When we have a complete object
                if bracket_count == 0:
                    # Remove leading comma and whitespace if present
                    clean_buffer = buffer.strip().lstrip(",").strip()
                    if clean_buffer:
                        try:
                            entry = json.loads(clean_buffer)
                            entries.append(entry)
                            buffer = ""
                        except json.JSONDecodeError:
                            # Skip malformed entries
                            buffer = ""

    return entries

def starsystem_generator(file_path: str) -> Dict:
    """
    Generator that yields entries one by one from a gzipped JSON file.
    Assumes the JSON file contains an array of objects.
    Assumes that each object is well-formed and contained within a single row.
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        # Skip the opening bracket
        f.read(1)  # Read '['

        buffer = ""
        bracket_count = 0
        in_string = False
        escape_next = False
        while True:
            char = f.read(1)
            if not char:  # End of file
                break

            buffer += char

            # Handle string literals (to ignore brackets inside strings)
            if escape_next:
                escape_next = False
                continue

            if char == "\\":
                escape_next = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            # Count brackets to find complete objects
            if char == "{":
                bracket_count += 1
            elif char == "}":
                bracket_count -= 1

                # When we have a complete object
                if bracket_count == 0:
                    # Remove leading comma and whitespace if present
                    clean_buffer = buffer.strip().lstrip(",").strip()
                    if clean_buffer:
                        try:
                            entry = json.loads(clean_buffer)
                            yield entry
                            buffer = ""
                        except json.JSONDecodeError:
                            # Skip malformed entries
                            buffer = ""


def estimate_total_entries(file_path: str, sample_size: int = 100) -> int:
    """
    Estimates the total number of entries by reading a sample and extrapolating.
    Much faster than counting all entries for very large files.
    """
    # Get file size
    file_size = os.path.getsize(file_path)

    # Read sample entries and calculate average size
    sample_entries = read_first_n_entries(file_path, sample_size)
    if not sample_entries:
        return 0

    # Calculate average entry size (rough approximation)
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        # Read a chunk that contains our sample
        chunk = f.read(50000)  # Read first 50KB

    # Estimate based on sample
    avg_entry_size = len(chunk) / len(sample_entries) if sample_entries else 1

    # Estimate total entries (very rough approximation)
    # Gzip compression ratio is typically 3:1 to 10:1 for JSON
    estimated_total = int(
        file_size / avg_entry_size * 5
    )  # Compression factor approximation

    return estimated_total


def header(bytes_count: int = 100) -> List[str]:
    print("=" * 60)
    print("Galaxy.json.gz File header")
    print("=" * 60)
    galaxy_file_path = "galaxy.json.gz"
    with gzip.open(galaxy_file_path, "rt", encoding="utf-8") as f:
        # Read first bytes_count bytes
        header_content = f.read(bytes_count).splitlines()
    return header_content


def main10rows():
    """Prints out the first 10 rows of the galaxy.json.gz file and estimates the total number of rows."""
    start_time = datetime.datetime.now()
    print("Starting to process galaxy.json.gz file...")

    galaxy_file_path = "galaxy.json.gz"

    # Check if file exists
    if not os.path.exists(galaxy_file_path):
        print(f"Error: {galaxy_file_path} not found!")
        return

    # Get file size
    file_size = os.path.getsize(galaxy_file_path)
    print(f"File size: {file_size / (1024**3):.2f} GB")

    # Read first 10 entries
    print("Reading first 10 entries...")
    first_entries = read_first_n_entries(galaxy_file_path, 10)

    print(f"\nFirst {len(first_entries)} entries from galaxy.json.gz:")
    print("=" * 60)

    for i, entry in enumerate(first_entries, 1):
        print(f"\nEntry {i}:")
        print(json.dumps(entry, indent=2))
        print("-" * 40)

    # Estimate total entries
    print("\nEstimating total entries...")
    try:
        estimated_total = estimate_total_entries(galaxy_file_path)
        print(f"\nEstimated total entries in galaxy.json.gz: {estimated_total:,}")
        print("(This is a rough approximation for the 9GB file)")
    except Exception as e:
        print(f"Error estimating entries: {e}")

    end_time = datetime.datetime.now()
    duration = get_duration(start_time, end_time)
    print(f"\nProcessing time: {duration}")


def maingenerator():
   """Use the generator to print first 10 entries."""
   generator = starsystem_generator("galaxy.json.gz")
   print("\nFirst 10 entries using generator:")
   for i, entry in enumerate(generator):
       if i >= 10:
           break
       print(json.dumps(entry, indent=2))
       print("-" * 40)

def main_populate():
    """Populate the database with entries from the galaxy.json.gz file."""
    from edgs_db import add_alliance_type, add_government_type, add_economy_type, add_stars_system_data
    from starsystemdata import StarSystemData

    start_time = datetime.datetime.now()
    print("Starting to populate the database from galaxy.json.gz file...")

    galaxy_file_path = "galaxy.json.gz"

    # Check if file exists
    if not os.path.exists(galaxy_file_path):
        print(f"Error: {galaxy_file_path} not found!")
        return

    generator = starsystem_generator(galaxy_file_path)
    count = 0
    for entry in generator:
        try:
            system_data = StarSystemData(
                SystemAddress=entry.get("SystemAddress"),
                StarSystem=entry.get("StarSystem"),
                StarPos_x=entry.get("StarPos", [0, 0, 0])[0],
                StarPos_y=entry.get("StarPos", [0, 0, 0])[1],
                StarPos_z=entry.get("StarPos", [0, 0, 0])[2],
            )
            add_stars_system_data(system_data)
            count += 1
            if count % 1000 == 0:
                print(f"{count} entries added to the database...")
        except Exception as e:
            print(f"Error processing entry: {e}")

    end_time = datetime.datetime.now()
    duration = get_duration(start_time, end_time)
    print(f"\nFinished populating database. Total entries added: {count}")
    print(f"Processing time: {duration}")

if __name__ == "__main__":
    maingenerator()
