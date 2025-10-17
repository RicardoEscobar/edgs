from typing import TypedDict

"""
 " database data dictionary
"""
class StarSystemData(TypedDict):
    SystemAddress: int | None
    StarSystem: str | None
    StarPos_x: float | None
    StarPos_y: float | None
    StarPos_z: float | None
