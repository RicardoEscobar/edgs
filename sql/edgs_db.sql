/*
EDGS SQL Database Schema
Version: 1.0
Author: Ricardo Escobar
Timestamp: 2025-10-17 18:20:30 UTC
Description: This SQL database schema is designed for the game Elite Dangerous, storing information about systems, stations, factions, and other game-related data to identify "glorious" systems and stations.
*/

-- Create the Database if it doesn't exist
DROP DATABASE IF EXISTS edgs;
CREATE DATABASE IF NOT EXISTS edgs;
USE edgs;

-- Table to store information about star systems
CREATE TABLE IF NOT EXISTS starsystem (
    SystemAddress BIGINT NOT NULL PRIMARY KEY,  
    StarSystem VARCHAR(255) NOT NULL,
    StarPos_x FLOAT NULL,
    StarPos_y FLOAT NULL,
    StarPos_z FLOAT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

SELECT * FROM edgs.starsystem;