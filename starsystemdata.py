from typing import TypedDict

"""
 " database data dictionary
"""
class StarSystemData(TypedDict):
    id: int | None
    StarSystem: str | None
    SystemAddress: int | None
    StarPos_x: float | None
    StarPos_y: float | None
    StarPos_z: float | None
