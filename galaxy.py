"""
This script explores a gigantic json file contained inside a galaxy.json.gz file and prints out the number of rows
contained inside.
"""

import json
import gzip
import datetime
from typing import Dict


def get_duration(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    duration = end_time - start_time
    # Format duration as a string hh:mm:ss
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def head(num_rows: int, data: list[dict]) -> None:
    """
    Prints the first num_rows entries from the data file
    """
    for i in range(min(num_rows, len(data))):
        print(data[i])


def main():
    """Prints out the first 10 rows of the galaxy.json.gz file and the total number of rows."""
    
    galaxy_file_path = "galaxy.json.gz"
    with gzip.open(galaxy_file_path, "rt", encoding="utf-8") as f:
        galaxy_data = json.load(f)

    num_rows = len(galaxy_data)
    print(f"The galaxy.json.gz file contains {num_rows} rows.")
    end_time = datetime.datetime.now()
    duration = get_duration(start_time, end_time)
    print(f"Processing time: {duration}")

if __name__ == "__main__":
    main()
