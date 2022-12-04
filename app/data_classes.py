from ast import List
from typing import Dict, Tuple
from pydantic import BaseModel

class Unit(BaseModel):
    name:str
    image_url:str
    unit_id:str
    base_id:str
    count: int | None
    
class GacSeason(BaseModel):
    type:str
    rounds:list[int]
    season:int
    startDate:str | None 
    endDate:str | None
    
class GacBattle(BaseModel):
    attackers: list[int]
    defenders: list[int] # too heavy to use Team = list[Unit]
    wins:int
    losses:int
    avg_banners:float
    win_percent:float

class StatLimit(BaseModel):
    stat_id: int
    stat_min: int
    stat_max: int
    stat_name: str | None

class DatacronCC(BaseModel):
    ability_3: int | None
    ability_6: int | None
    ability_9: int | None
    stat_limits: list[StatLimit]


class Team(BaseModel):
    leader: Unit
    members: list[Unit]
    datacron: DatacronCC | None
    stat_limits: list[StatLimit] | None

class GacDataRequest(BaseModel):
    season:GacSeason
    attackers: Team | None 
    defenders: Team | None
    cutoff: int | None

class GacBattleData(BaseModel):
    battles: list[GacBattle]

    battlesCCin:  list[dict] | None  # recursion is not supported fully
    battlesCCout: list[dict] | None

# class DCSLRow(BaseModel):
#     id: int
#     count: int
#     long_desc: str

# class DCSeasonList(BaseModel):
#     season:int
#     l3: list[DCSLRow]
#     l6: list[DCSLRow]
#     l9: list[DCSLRow]

#class PopularLeaders(BaseModel):
#    attackers: list[int]
#    defenders: list[int]

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



