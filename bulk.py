"""
This script makes a bulk insert of star systems from the galaxy.json.gz file into the database.
"""

import json
import gzip
import datetime
from typing import Dict
from edgs_db import add_stars_system_data_bulk, get_catalog_type_dict
from starsystemdata import StarSystemData
from galaxy_efficient import starsystem_generator


def get_duration(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    duration = end_time - start_time
    # Format duration as a string hh:mm:ss
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def insert_bulk(file_path: str, bulk_size: int):
    """
    Reads the galaxy.json.gz file and returns a list of StarSystemData dictionaries for bulk insertion.
    """
    star_systems_bulk = starsystem_generator(file_path)

    # Retrieve catalog type dictionaries
    alliance_dict = get_catalog_type_dict("AllianceType")
    government_dict = get_catalog_type_dict("GovernmentType")
    economy_dict = get_catalog_type_dict("EconomyType")
    security_dict = get_catalog_type_dict("SecurityType")

    # Form a list of StarSystemData dictionaries
    star_systems_data_list: list[StarSystemData] = []
    # Iterate through star systems and create StarSystemData objects using bulk_size to limit memory usage
    for star_system in star_systems_bulk:
        star_system_data: StarSystemData = {
            "id64": star_system["id64"],
            "name": star_system["name"],
            "coords_x": star_system["coords"]["x"],
            "coords_y": star_system["coords"]["y"],
            "coords_z": star_system["coords"]["z"],
            "allegiance_id": alliance_dict.get(star_system.get("allegiance", None)),
            "government_id": government_dict.get(star_system.get("government", None)),
            "primary_economy_id": economy_dict.get(star_system.get("primaryEconomy", None)),
            "secondary_economy_id": economy_dict.get(star_system.get("secondaryEconomy", None)),
            "security_id": security_dict.get(star_system.get("security", None)),
            "population": star_system.get("population", 0),
            "date": datetime.datetime.now(),
        }
        star_systems_data_list.append(star_system_data)

        # If we reached the bulk size, insert into the database
        if len(star_systems_data_list) >= bulk_size:
            add_stars_system_data_bulk(star_systems_data_list)
            star_systems_data_list = []  # Reset for the next batch

    # Insert any remaining data
    if star_systems_data_list:
        add_stars_system_data_bulk(star_systems_data_list)

def main():
    """Main function to perform bulk insertion."""
    galaxy_file_path = "galaxy.json.gz"
    bulk_size = 1000  # Define the bulk size for insertion

    start_time = datetime.datetime.now()
    print("Starting bulk insertion...")
    insert_bulk(galaxy_file_path, bulk_size)
    end_time = datetime.datetime.now()

    duration = get_duration(start_time, end_time)
    print(f"Bulk insertion completed in {duration}.")

if __name__ == "__main__":
    main()
