"""
This script explores a gigantic json file contained inside a galaxy.json.gz file and saves in a list the names of all alliances.
"""

import json
import gzip
from typing import List

from galaxy_efficient import starsystem_generator


def extract_alliance_names(file_path: str) -> List[str]:
    """
    Extracts the names of all alliances from the galaxy.json.gz file.
    """
    alliance_names = set()

    for star_system in starsystem_generator(file_path):
        alliance = star_system.get("allegiance")
        if alliance:
            alliance_names.add(alliance)
        # print last processed alliance name if was added successfully
            print(f"Processed alliance: {alliance}")

    return sorted(alliance_names)


def main():
    galaxy_file_path = "galaxy.json.gz"
    alliance_names = extract_alliance_names(galaxy_file_path)



if __name__ == "__main__":
    main()
