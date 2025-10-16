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
