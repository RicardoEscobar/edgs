# Elite Dangerous Glorious Systems (EDGS)

Is a SQL database for the game Elite Dangerous, it stores information about systems, stations, factions, and other game-related data to identify "glorious" systems and stations.

# What is a "Glorious System"?

A glorious system is defined by the following criteria:

- Pending Expansion state, or recently (less than 3 days) in Expansion state
- Economy: Agriculture or Agriculture/Industrial
- Controlling faction: Is a player faction.
- The controlling faction's influence is >= 0.75 (75 %)
- Population >= 1,000,000
- With at least 5 (This number can vary) star ports and/or planetary ports of Agriculture/Industrial economy.

# Why?

Glorious systems are ideal for players looking to make obscene amounts of money quickly. They offer high-value Mining Expansion Missions, with payouts that can reach into 50,000,000 credits for a single mission. Using a Panther Clipper MK2, players can efficiently complete these missions on a single trip, making it a lucrative endeavor.

# TODO

## Connect to EDSM API to get more data (NOT WORKING)

This has proven to be innefective since the API has bugs and is unusable at this point.

## Connect directly to EDDN to get real-time data

This is more like it. We can get real-time data from EDDN and update our database accordingly. We need to implement a listener for EDDN and process the data as it comes in. Then we can update our database with the new data.

## Design and create a relational database schema

We need to design a database schema that can store all the relevant data about systems, stations, factions, and other game-related data. We can use MariaDB for this purpose. Also using SQLite3 for local testing and sharing the database downloading it from the repo.

# AI analysis

Based on my analysis of all the schema README files, I can now provide you with a comprehensive breakdown of which schemas are related to systems, bodies, stations, and factions in Elite Dangerous:

## EDDN Schema Classification for Elite Dangerous Game Elements
### Systems (Star Systems)
- journal - Covers FSDJump, Location, and CarrierJump events that contain system-level data including system names, coordinates, and faction information
- navroute - Navigation route data between systems
- fssdiscoveryscan - Full Spectrum System Scanner discovery scan data for systems
- fssallbodiesfound - When all bodies in a system have been discovered via FSS
- navbeaconscan - Navigation beacon scan data within systems
### Bodies (Planets, Stars, etc.)
- journal - Covers Scan events for detailed body scan data (planets, stars, moons)
- scanbarycentre - Scans of barycentre objects (gravitational centers of binary systems)
- fssbodysignals - Signals detected on specific bodies via Full Spectrum Scanner
- fsssignaldiscovered - Various signals discovered via FSS, often body-related
- codexentry - Codex discoveries often related to biological or geological features on bodies
- approachsettlement - When approaching settlements on planetary bodies
### Stations (Markets, Docking, Services)
- commodity - Market data from stations including commodity prices and availability
- outfitting - Station outfitting services and available modules
- shipyard - Station shipyard services and available ships
- dockinggranted - Successful docking permissions at stations
- dockingdenied - Failed docking attempts at stations
- fcmaterials_capi - Fleet Carrier materials data (stations are essentially mobile stations)
- fcmaterials_journal - Fleet Carrier materials from journal events
- blackmarket - (Deprecated) Black market data from stations
### Factions
- journal - The main source for faction data through FSDJump, Location, and Docked events which include faction information for systems and stations
- codexentry - May contain faction-related discoveries

### Additional Notes:
The journal schema is the most comprehensive, covering multiple game elements including systems, bodies, stations, and factions through various journal events (Docked, FSDJump, Scan, Location, SAASignalsFound, CarrierJump)
Many schemas require augmentation with system coordinates (StarPos) and system names (StarSystem) from location-tracking events
The blackmarket schema is deprecated in favor of the commodity schema's prohibited array
Several schemas are specifically for exploration data (FSS-related schemas, scan schemas) that primarily deal with systems and bodies
Station-related schemas focus on services and market data rather than the physical characteristics of the stations themselves
This classification helps understand which schemas provide data about the core game elements that make up the Elite Dangerous galaxy.