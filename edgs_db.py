"""
This module handles database interactions for the EDGS application.
The database engine is MariaDB, and this module provides functions to connect,
query, and manage the database.
"""

import os

import mysql.connector as database
from dotenv import load_dotenv

from starsystemdata import StarSystemData

# Database connection parameters
load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
database_name = os.getenv("database")

# Establish a connection to the database
connection = database.connect(
    user=user, password=password, host=host, database=database_name
)

# Define a cursor for executing queries
cursor = connection.cursor()


def get_catalog_type_dict(catalog_name: str) -> dict[str, int]:
    """
    Retrieves all catalog types from the database and returns a dictionary mapping names to IDs.
    """
    catalog_dict = {}
    try:
        statement = f"SELECT id, name FROM {catalog_name}"
        cursor.execute(statement)
        results = cursor.fetchall()
        for row in results:
            catalog_dict[row[1]] = row[0]
    except database.Error as e:
        print(f"Error retrieving catalog types: {e}")
    return catalog_dict


# Function to add data to the database (single record)
def add_stars_system_data(stars_system_data: StarSystemData):
    """
    Adds a new star system record to the database.
    """
    try:
        statement = (
            "INSERT INTO StarSystem (id64, name, coords_x, coords_y, coords_z, allegiance_id, government_id, primary_economy_id, secondary_economy_id, security_id, population, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "name=VALUES(name), coords_x=VALUES(coords_x), coords_y=VALUES(coords_y), coords_z=VALUES(coords_z), allegiance_id=VALUES(allegiance_id), government_id=VALUES(government_id), primary_economy_id=VALUES(primary_economy_id), secondary_economy_id=VALUES(secondary_economy_id), security_id=VALUES(security_id), population=VALUES(population), date=VALUES(date)"
        )
        data = (
            stars_system_data["id64"],
            stars_system_data["name"],
            stars_system_data["coords_x"],
            stars_system_data["coords_y"],
            stars_system_data["coords_z"],
            stars_system_data["allegiance_id"],
            stars_system_data["government_id"],
            stars_system_data["primary_economy_id"],
            stars_system_data["secondary_economy_id"],
            stars_system_data["security_id"],
            stars_system_data["population"],
            stars_system_data["date"],
        )
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")


# Function to add multiple records in bulk (much more efficient)
def add_stars_system_data_bulk(stars_system_data_list: list[StarSystemData], batch_size: int = 1000):
    """
    Adds multiple star system records to the database in bulk for better performance.
    
    Args:
        stars_system_data_list: List of StarSystemData dictionaries
        batch_size: Number of records to insert in each batch (default 1000)
    """

    try:
        statement = (
            "INSERT INTO StarSystem (id64, name, coords_x, coords_y, coords_z, allegiance_id, government_id, primary_economy_id, secondary_economy_id, security_id, population, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "name=VALUES(name), coords_x=VALUES(coords_x), coords_y=VALUES(coords_y), coords_z=VALUES(coords_z), allegiance_id=VALUES(allegiance_id), government_id=VALUES(government_id), primary_economy_id=VALUES(primary_economy_id), secondary_economy_id=VALUES(secondary_economy_id), security_id=VALUES(security_id), population=VALUES(population), date=VALUES(date)"
        )
        
        total_records = len(stars_system_data_list)
        inserted_count = 0
        
        # Process in batches for memory efficiency
        for i in range(0, total_records, batch_size):
            batch = stars_system_data_list[i:i + batch_size]
            
            # Prepare batch data
            batch_data = []
            for system_data in batch:
                data_tuple = (
                    system_data["id64"],
                    system_data["name"],
                    system_data["coords_x"],
                    system_data["coords_y"],
                    system_data["coords_z"],
                    system_data["allegiance_id"],
                    system_data["government_id"],
                    system_data["primary_economy_id"],
                    system_data["secondary_economy_id"],
                    system_data["security_id"],
                    system_data["population"],
                    system_data["date"],
                )
                batch_data.append(data_tuple)
            
            # Execute batch insert
            cursor.executemany(statement, batch_data)
            connection.commit()
            
            inserted_count += len(batch)

        print(f"Successfully added {total_records} entries to database in bulk")
        
    except database.Error as e:
        print(f"Error adding bulk entries to database: {e}")
        # Rollback in case of error
        connection.rollback()


# Function to get data from the database
def get_data() -> list[StarSystemData]:
    """
    Retrieves all star system records from the database.
    """
    resultset = []
    try:
        statement = "SELECT id64, name, coords_x, coords_y, coords_z FROM StarSystem"
        cursor.execute(statement)
        results = cursor.fetchall()
        for row in results:
            system_data = StarSystemData(
                id64=row[0],  # SystemAddress is in column 0
                name=row[1],  # StarSystem is in column 1
                coords_x=row[2],  # StarPos_x is in column 2
                coords_y=row[3],  # StarPos_y is in column 3
                coords_z=row[4],  # StarPos_z is in column 4
            )
            resultset.append(system_data)
    except database.Error as e:
        print(f"Error retrieving data from database: {e}")
    return resultset


def main():
    # Test get_catalog_type_dict function
    alliance_dict = get_catalog_type_dict("AllianceType")
    government_dict = get_catalog_type_dict("GovernmentType")
    economy_dict = get_catalog_type_dict("EconomyType")
    security_dict = get_catalog_type_dict("SecurityType")

    # Example usage - single record
    add_stars_system_data(
        {
            "id64": 123456789,
            "name": "Sol",
            "coords_x": 0.0,
            "coords_y": 0.0,
            "coords_z": 0.0,
            "allegiance_id": alliance_dict.get("Federation", None),
            "government_id": government_dict.get("Democracy", None),
            "primary_economy_id": economy_dict.get("Industrial", None),
            "secondary_economy_id": economy_dict.get("Agricultural", None),
            "security_id": security_dict.get("High", None),
            "population": 10000000000,
            "date": "2024-01-01 00:00:00",
        }
    )
    
    # Example usage - bulk insert (much more efficient for large datasets)
    sample_systems = [
        {
            "id64": 123456790,
            "name": "Alpha Centauri",
            "coords_x": 1.25,
            "coords_y": 2.34,
            "coords_z": 3.45,
            "allegiance_id": alliance_dict.get("Federation", None),
            "government_id": government_dict.get("Democracy", None),
            "primary_economy_id": economy_dict.get("Industrial", None),
            "secondary_economy_id": economy_dict.get("Agricultural", None),
            "security_id": security_dict.get("High", None),
            "population": 5000000000,
            "date": "2024-01-01 00:00:00",
        },
        {
            "id64": 123456791,
            "name": "Wolf 359",
            "coords_x": 7.86,
            "coords_y": 0.31,
            "coords_z": -2.73,
            "allegiance_id": alliance_dict.get("Independent", None),
            "government_id": government_dict.get("Anarchy", None),
            "primary_economy_id": economy_dict.get("Extraction", None),
            "secondary_economy_id": None,
            "security_id": security_dict.get("Low", None),
            "population": 1000000,
            "date": "2024-01-01 00:00:00",
        }
    ]
    
    # Insert multiple records at once
    add_stars_system_data_bulk(sample_systems)
    
    systems = get_data()
    for system in systems:
        print(system)

    connection.close()


if __name__ == "__main__":
    main()
