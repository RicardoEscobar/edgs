#!/usr/bin/env python3

"""
EDDN Subscriber to get systems, bodies, stations and factions data.
By Ricardo Escobar
2025-10-16 16:24:19 UTC

This script listens to EDDN for:
- Star system names and coordinates
- Planet and celestial body data
- Exploration scan results
- Navigation routes between systems
- Station data (services, facilities, etc.)
- Faction information and influence data

Installation:
pip install pyzmq
pip install simplejson
"""

import sys, os, datetime, time
from typing import TypedDict

import zlib
import zmq
import simplejson

from edgs_db import add_data, get_data
from starsystemdata import StarSystemData

"""
 "  Configuration
"""
__relayEDDN = "tcp://eddn.edcd.io:9500"
__timeoutEDDN = 600000

# Set False to listen to production stream
__debugEDDN = False

# Set to False if you do not want verbose logging
__logVerboseFile = os.path.dirname(__file__) + "/Logs_Verbose_EDDN_%DATE%.htm"
# __logVerboseFile        = False

# Set to False if you do not want JSON logging
__logJSONFile = os.path.dirname(__file__) + "/Logs_JSON_EDDN_%DATE%.log"
# __logJSONFile           = False

# A sample list of authorised softwares
__authorisedSoftwares = [
    "E:D Market Connector",
    "EDDiscovery",
    "EDDI",
    "EDCE",
    "ED-TD.SPACE",
    "EliteOCR",
    "Maddavo's Market Share",
    "RegulatedNoise",
    "RegulatedNoise__DJ",
]

# Used this to excludes yourself for example has you don't want to handle your own messages ^^
__excludedSoftwares = ["My Awesome Market Uploader"]


"""
 "  Start
"""


def date(__format):
    d = datetime.datetime.now(datetime.timezone.utc)
    return d.strftime(__format)


__oldTime = False


def echoLog(__str):
    global __oldTime, __logVerboseFile

    if __logVerboseFile != False:
        __logVerboseFileParsed = __logVerboseFile.replace(
            "%DATE%", str(date("%Y-%m-%d"))
        )

    if __logVerboseFile != False and not os.path.exists(__logVerboseFileParsed):
        f = open(__logVerboseFileParsed, "w")
        f.write(
            '<style type="text/css">html { white-space: pre; font-family: Courier New,Courier,Lucida Sans Typewriter,Lucida Typewriter,monospace; }</style>'
        )
        f.close()

    if (__oldTime == False) or (__oldTime != date("%H:%M:%S")):
        __oldTime = date("%H:%M:%S")
        __str = str(__oldTime) + " | " + str(__str)
    else:
        __str = "        " + " | " + str(__str)

    print(__str)
    sys.stdout.flush()

    if __logVerboseFile != False:
        f = open(__logVerboseFileParsed, "a")
        f.write(__str + "\n")
        f.close()


def echoLogJSON(__json):
    global __logJSONFile

    if __logJSONFile != False:
        __logJSONFileParsed = __logJSONFile.replace("%DATE%", str(date("%Y-%m-%d")))

        f = open(__logJSONFileParsed, "a")
        f.write(str(__json) + "\n")
        f.close()


def main():
    echoLog("Starting EDDN Subscriber")
    echoLog("")

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    while True:
        try:
            subscriber.connect(__relayEDDN)
            echoLog("Connect to " + __relayEDDN)
            echoLog("")
            echoLog("")

            while True:
                __message = subscriber.recv()

                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    echoLog("Disconnect from " + __relayEDDN)
                    echoLog("")
                    echoLog("")
                    break

                echoLog("Got a message")

                __message = zlib.decompress(__message)
                if __message == False:
                    echoLog("Failed to decompress message")

                __json = simplejson.loads(__message)
                if __json == False:
                    echoLog("Failed to parse message as json")

                __converted = False

                # Handle Journal events (exploration data)
                if __json["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving journal message...")

                    __authorised = False
                    __excluded = False

                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True
                    if __json["header"]["softwareName"] in __excludedSoftwares:
                        __excluded = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )
                    echoLog(
                        "        - "
                        + (
                            "AUTHORISED"
                            if (__authorised == True)
                            else (
                                "EXCLUDED" if (__excluded == True) else "UNAUTHORISED"
                            )
                        )
                    )

                    if __authorised == True and __excluded == False:
                        __event = __json["message"]["event"]
                        echoLog("    - Event: " + __event)
                        echoLog("    - Timestamp: " + __json["message"]["timestamp"])
                        echoLog("    - Uploader ID: " + __json["header"]["uploaderID"])

                        # Create empty StarSystemData object
                        star_system_data: StarSystemData = {
                            "id": None,
                            "StarSystem": None,
                            "address": None,
                            "StarPos_x": None,
                            "StarPos_y": None,
                            "StarPos_z": None,
                        }

                        # Handle different journal events
                        if __event == "FSDJump":
                            echoLog(
                                "        - System Name: "
                                + __json["message"]["StarSystem"]
                            )

                            if "SystemAddress" in __json["message"]:
                                echoLog(
                                    "        - System Address: "
                                    + str(__json["message"]["SystemAddress"])
                                )

                            if "StarPos" in __json["message"]:
                                echoLog(
                                    "        - Star Position: "
                                    + str(__json["message"]["StarPos"])
                                )

                        elif __event == "Scan":
                            echoLog(
                                "        - Body Name: " + __json["message"]["BodyName"]
                            )
                            if "StarSystem" in __json["message"]:
                                echoLog(
                                    "        - System Name: "
                                    + __json["message"]["StarSystem"]
                                )
                            if "BodyType" in __json["message"]:
                                echoLog(
                                    "        - Body Type: "
                                    + __json["message"]["BodyType"]
                                )
                            if "PlanetClass" in __json["message"]:
                                echoLog(
                                    "        - Planet Class: "
                                    + __json["message"]["PlanetClass"]
                                )

                        elif __event == "Location":
                            echoLog(
                                "        - System Name: "
                                + __json["message"]["StarSystem"]
                            )
                            if "SystemAddress" in __json["message"]:
                                echoLog(
                                    "        - System Address: "
                                    + str(__json["message"]["SystemAddress"])
                                )
                            if "StarPos" in __json["message"]:
                                echoLog(
                                    "        - Star Position: "
                                    + str(__json["message"]["StarPos"])
                                )
                            # Station information if docked
                            if (
                                "Docked" in __json["message"]
                                and __json["message"]["Docked"]
                            ):
                                if "StationName" in __json["message"]:
                                    echoLog(
                                        "        - Docked at Station: "
                                        + __json["message"]["StationName"]
                                    )
                                if "StationType" in __json["message"]:
                                    echoLog(
                                        "        - Station Type: "
                                        + __json["message"]["StationType"]
                                    )
                            # Faction information
                            if "SystemFaction" in __json["message"]:
                                faction = __json["message"]["SystemFaction"]
                                if "Name" in faction:
                                    echoLog(
                                        "        - Controlling Faction: "
                                        + faction["Name"]
                                    )
                                if "FactionState" in faction:
                                    echoLog(
                                        "        - Faction State: "
                                        + faction["FactionState"]
                                    )
                            if "Factions" in __json["message"]:
                                echoLog(
                                    "        - System Factions ("
                                    + str(len(__json["message"]["Factions"]))
                                    + "):"
                                )
                                for faction in __json["message"]["Factions"][
                                    :3
                                ]:  # Limit to first 3 factions
                                    if "Name" in faction:
                                        influence = faction.get("Influence", "Unknown")
                                        state = faction.get("FactionState", "Unknown")
                                        echoLog(
                                            "          - "
                                            + faction["Name"]
                                            + " (Influence: "
                                            + str(influence)
                                            + ", State: "
                                            + state
                                            + ")"
                                        )

                        elif __event == "Docked":
                            if "StarSystem" in __json["message"]:
                                echoLog(
                                    "        - System Name: "
                                    + __json["message"]["StarSystem"]
                                )
                            echoLog(
                                "        - Station Name: "
                                + __json["message"]["StationName"]
                            )
                            if "StationType" in __json["message"]:
                                echoLog(
                                    "        - Station Type: "
                                    + __json["message"]["StationType"]
                                )
                            if "MarketID" in __json["message"]:
                                echoLog(
                                    "        - Market ID: "
                                    + str(__json["message"]["MarketID"])
                                )
                            # Station services
                            if "StationServices" in __json["message"]:
                                services = ", ".join(
                                    __json["message"]["StationServices"][:5]
                                )  # Limit to first 5
                                echoLog("        - Services: " + services)
                            # Station faction
                            if "StationFaction" in __json["message"]:
                                faction = __json["message"]["StationFaction"]
                                if "Name" in faction:
                                    echoLog(
                                        "        - Station Faction: " + faction["Name"]
                                    )

                        elif __event in ["FactionKillBond", "Bounty"]:
                            if "StarSystem" in __json["message"]:
                                echoLog(
                                    "        - System Name: "
                                    + __json["message"]["StarSystem"]
                                )
                            if "VictimFaction" in __json["message"]:
                                echoLog(
                                    "        - Victim Faction: "
                                    + __json["message"]["VictimFaction"]
                                )
                            if "AwardingFaction" in __json["message"]:
                                echoLog(
                                    "        - Awarding Faction: "
                                    + __json["message"]["AwardingFaction"]
                                )

                    del __authorised, __excluded
                    echoLog("")
                    echoLog("")

                # Handle NavRoute events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/navroute/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving navroute message...")

                    __authorised = False
                    __excluded = False

                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True
                    if __json["header"]["softwareName"] in __excludedSoftwares:
                        __excluded = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )

                    if __authorised == True and __excluded == False:
                        echoLog("    - Timestamp: " + __json["message"]["timestamp"])
                        if "Route" in __json["message"]:
                            echoLog(
                                "    - Route with "
                                + str(len(__json["message"]["Route"]))
                                + " systems:"
                            )
                            for i, system in enumerate(__json["message"]["Route"]):
                                echoLog(
                                    "        "
                                    + str(i + 1)
                                    + ". "
                                    + system["StarSystem"]
                                )
                                if "SystemAddress" in system:
                                    echoLog(
                                        "           Address: "
                                        + str(system["SystemAddress"])
                                    )

                    del __authorised, __excluded
                    echoLog("")
                    echoLog("")

                # Handle FSS Discovery Scan events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/fssdiscoveryscan/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving FSS discovery scan message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "BodyCount" in __json["message"]:
                            echoLog(
                                "    - Body Count: "
                                + str(__json["message"]["BodyCount"])
                            )
                        if "NonBodyCount" in __json["message"]:
                            echoLog(
                                "    - Non-Body Count: "
                                + str(__json["message"]["NonBodyCount"])
                            )

                    echoLog("")

                # Handle FSS Signal Discovered events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/fsssignaldiscovered/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving FSS signal discovered message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )
                    echoLog(
                        "        - "
                        + ("AUTHORISED" if __authorised else "UNAUTHORISED")
                    )

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "SignalName" in __json["message"]:
                            echoLog(
                                "    - Signal Name: " + __json["message"]["SignalName"]
                            )

                    echoLog("")

                # Handle Docking Granted events (station data)
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/dockinggranted/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving docking granted message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )
                    echoLog(
                        "        - "
                        + ("AUTHORISED" if __authorised else "UNAUTHORISED")
                    )

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "StationName" in __json["message"]:
                            echoLog(
                                "    - Station Name: "
                                + __json["message"]["StationName"]
                            )
                        if "StationType" in __json["message"]:
                            echoLog(
                                "    - Station Type: "
                                + __json["message"]["StationType"]
                            )
                        if "MarketID" in __json["message"]:
                            echoLog(
                                "    - Market ID: " + str(__json["message"]["MarketID"])
                            )

                    echoLog("")

                # Handle Approach Settlement events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/approachsettlement/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving approach settlement message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "Name" in __json["message"]:
                            echoLog(
                                "    - Settlement Name: " + __json["message"]["Name"]
                            )
                        if "BodyName" in __json["message"]:
                            echoLog("    - Body Name: " + __json["message"]["BodyName"])

                    echoLog("")

                # Handle FSS Body Signals events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/fssbodysignals/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving FSS body signals message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "BodyName" in __json["message"]:
                            echoLog("    - Body Name: " + __json["message"]["BodyName"])
                        if "Signals" in __json["message"]:
                            echoLog(
                                "    - Signals found: "
                                + str(len(__json["message"]["Signals"]))
                            )
                            for signal in __json["message"]["Signals"]:
                                if "Type" in signal:
                                    echoLog("      - Signal Type: " + signal["Type"])

                    echoLog("")

                # Handle Scan Barycentre events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/scanbarycentre/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving scan barycentre message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "BodyName" in __json["message"]:
                            echoLog("    - Body Name: " + __json["message"]["BodyName"])

                    echoLog("")

                # Handle Codex Entry events
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/codexentry/1" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving codex entry message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    if __authorised:
                        if "StarSystem" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["StarSystem"]
                            )
                        if "Name" in __json["message"]:
                            echoLog(
                                "    - Discovery Name: " + __json["message"]["Name"]
                            )
                        if "Category" in __json["message"]:
                            echoLog("    - Category: " + __json["message"]["Category"])

                    echoLog("")

                # Handle Commodity v3 events (market data)
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/commodity/3" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving commodity message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )
                    echoLog(
                        "        - "
                        + ("AUTHORISED" if __authorised else "UNAUTHORISED")
                    )

                    if __authorised:
                        if "systemName" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["systemName"]
                            )
                        if "stationName" in __json["message"]:
                            echoLog(
                                "    - Station Name: "
                                + __json["message"]["stationName"]
                            )
                        if "commodities" in __json["message"]:
                            echoLog(
                                "    - Commodities: "
                                + str(len(__json["message"]["commodities"]))
                                + " items"
                            )

                    echoLog("")

                # Handle Outfitting events (ship modules/equipment)
                elif __json[
                    "$schemaRef"
                ] == "https://eddn.edcd.io/schemas/outfitting/2" + (
                    "/test" if (__debugEDDN == True) else ""
                ):
                    echoLogJSON(__message)
                    echoLog("Receiving outfitting message...")

                    __authorised = False
                    if __json["header"]["softwareName"] in __authorisedSoftwares:
                        __authorised = True

                    echoLog(
                        "    - Software: "
                        + __json["header"]["softwareName"]
                        + " / "
                        + __json["header"]["softwareVersion"]
                    )
                    echoLog(
                        "        - "
                        + ("AUTHORISED" if __authorised else "UNAUTHORISED")
                    )

                    if __authorised:
                        if "systemName" in __json["message"]:
                            echoLog(
                                "    - System Name: " + __json["message"]["systemName"]
                            )
                        if "stationName" in __json["message"]:
                            echoLog(
                                "    - Station Name: "
                                + __json["message"]["stationName"]
                            )
                        if "modules" in __json["message"]:
                            echoLog(
                                "    - Modules available: "
                                + str(len(__json["message"]["modules"]))
                            )

                    echoLog("")

                # Handle unknown schemas
                else:
                    echoLog("Unknown schema: " + __json["$schemaRef"])

                del __converted

        except zmq.ZMQError as e:
            echoLog("")
            echoLog("ZMQSocketException: " + str(e))
            subscriber.disconnect(__relayEDDN)
            echoLog("Disconnect from " + __relayEDDN)
            echoLog("")
            time.sleep(5)


if __name__ == "__main__":
    main()
