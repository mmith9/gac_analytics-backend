from ast import List
from typing import Dict, Tuple
from pydantic import BaseModel

class Unit(BaseModel):
    name:str
    image_url:str
    unit_id:str
    base_id:str

class UnitFreq(Unit):
    count: int | None
    
class Team(BaseModel):
    leader: Unit
    members: list[Unit]


class GacSeason(BaseModel):
    type:str
    rounds:list[int]
    season:int
    startDate:str | None 
    endDate:str | None
    

# return? objects
class GacBattle(BaseModel):
    attackers: list[int]
    defenders: list[int]  # too heavy to use Team = list[Unit]
    wins: int
    losses: int
    avg_banners: float
    win_percent: float

class GacBattleData(BaseModel):
    battles: list[GacBattle]
    battlesCCin:  list[dict] | None 
    battlesCCout: list[dict] | None

class Freq(BaseModel):
    id: int
    count: int

class PORow(BaseModel):
    id: int
    count: int
    name: str | None
    max_value: float | None
    opt1: str | None
    units: list[Freq] | None

class PrecalcObject(BaseModel):
    season: int
    item_type: str
    payload: list[PORow]


# frontent classes, also data request model



class StatLimit(BaseModel):
    stat_id: int
    stat_min: int
    stat_max: int

class DatacronCC(BaseModel):
    ability_3: int | None
    ability_6: int | None
    ability_9: int | None
    stat_limits: list[StatLimit]

class UnitCC(BaseModel):
    unit_id: int
    stat_limits: list[StatLimit] | None

class TeamCC(BaseModel):
    leader: UnitCC | None
    members: list[UnitCC]
    datacron: DatacronCC | None

class WinCC(BaseModel):
    attempt: list[int] | None
    defenders_start: list[int]
    defenders_end: list[int]

class GacDataRequest(BaseModel):
    season: GacSeason
    attackers: TeamCC | None
    defenders: TeamCC | None
    win_conditions: WinCC | None
    cutoff: int | None



