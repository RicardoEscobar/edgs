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

user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
database_name = os.getenv('database')

# Establish a connection to the database
connection = database.connect(
    user=user, password=password, host=host, database=database_name
)

# Define a cursor for executing queries
cursor = connection.cursor()

# Function to add data to the database
def add_data(stars_system_data: StarSystemData):
    """
    Adds a new employee record to the database.
    """
    try:
        statement = "INSERT INTO starsystem (id, StarSystem, address, StarPos_x, StarPos_y, StarPos_z) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stars_system_data['id'], stars_system_data['StarSystem'], stars_system_data['address'],
                stars_system_data['StarPos_x'], stars_system_data['StarPos_y'], stars_system_data['StarPos_z'])
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

# Function to get data from the database
def get_data() -> list[StarSystemData]:
    """
    Retrieves all star system records from the database.
    """
    resultset = []
    try:
        statement = "SELECT * FROM starsystem"
        cursor.execute(statement)
        results = cursor.fetchall()
        for row in results:
            system_data = StarSystemData(
                id=row[0],
                StarSystem=row[1],
                address=row[2],
                StarPos_x=row[3],
                StarPos_y=row[4],
                StarPos_z=row[5]
            )
            resultset.append(system_data)
    except database.Error as e:
        print(f"Error retrieving data from database: {e}")
    return resultset


def main():
    # Example usage
    add_data({
        'id': 1,
        'StarSystem': 'Chaxiraxi',
        'SystemAddress': 16063849047465,
        'StarPos_x': -9.84375,
        'StarPos_y': 66.53125,
        'StarPos_z': 5.75
    })
    systems = get_data()
    for system in systems:
        print(system)

    connection.close()

if __name__ == "__main__":
    main()
