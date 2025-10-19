from typing import TypedDict

"""
 " database data dictionary
"""
class StarSystemData(TypedDict):
    id64: int | None
    name: str | None
    coords_x: float | None
    coords_y: float | None
    coords_z: float | None
    allegiance_id: int | None
    government_id: int | None
    primary_economy_id: int | None
    secondary_economy_id: int | None
    security_id: int | None
    population: int | None
    date: str | None
