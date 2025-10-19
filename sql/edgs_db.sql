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

-- Refactor: Create tables to store alliance, government, economy, and security types
CREATE TABLE AllianceType (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE GovernmentType (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE EconomyType (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE SecurityType (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

-- StarSystem table
CREATE TABLE StarSystem (
    id64 BIGINT PRIMARY KEY,
    name VARCHAR(255),
    coords_x FLOAT NULL,
    coords_y FLOAT NULL,
    coords_z FLOAT NULL,
    allegiance_id INT NULL,
    government_id INT NULL,
    primary_economy_id INT NULL,
    secondary_economy_id INT NULL,
    security_id INT NULL,
    population BIGINT,
    date TIMESTAMP,
    FOREIGN KEY (allegiance_id) REFERENCES AllianceType(id),
    FOREIGN KEY (government_id) REFERENCES GovernmentType(id),
    FOREIGN KEY (primary_economy_id) REFERENCES EconomyType(id),
    FOREIGN KEY (secondary_economy_id) REFERENCES EconomyType(id),
    FOREIGN KEY (security_id) REFERENCES SecurityType(id)
);

-- Populate catalog tables with initial data
INSERT INTO AllianceType (name) VALUES
('Independent'),
('Alliance'),
('Empire'),
('Federation'),
('Pirate'),
('Pilot\'s Federation'),
('Thargoids'),
('Guardian'),
('None');

INSERT INTO GovernmentType (name) VALUES
('Anarchy'),
('Colony'),
('Communism'),
('Confederacy'),
('Cooperative'),
('Corporate'),
('Democracy'),
('Dictatorship'),
('Feudal'),
('Patronage'),
('Prison'),
('Prison Colony'),
('Theocracy'),
('Engineer'),
('Private Ownership'),
('None');

INSERT INTO EconomyType (name) VALUES
('Agriculture'),
('Colony'),
('Damaged'),
('Engineer'),
('Extraction'),
('Industrial'),
('High Tech'),
('Military'),
('Prison'),
('Private Enterprise'),
('Refinery'),
('Repair'),
('Rescue'),
('Terraforming'),
('Tourism'),
('Under Attack'),
('None');

INSERT INTO SecurityType (name) VALUES
('Low'),
('Medium'),
('High'),
('Anarchy'),
('None');