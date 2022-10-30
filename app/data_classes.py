from ast import List
from typing import Dict, Tuple
from pydantic import BaseModel

class Unit(BaseModel):
    name:str
    image_url:str
    unit_id:str
    base_id:str
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
    
class GacBattle(BaseModel):
    attackers: list[int]
    defenders: list[int] # too heavy to use Team = list[Unit]
    wins:int
    losses:int
    avg_banners:float
    win_percent:float

class CC(BaseModel):
    type: str
    value: str

class GacDataRequest(BaseModel):
    season:GacSeason
    attackers: Team | None 
    defenders: Team | None
    constraints: list[CC] | None
    cutoff: int | None

class DatacronCC(BaseModel):
    side: str | None
    ability_3: int | None
    ability_6: int | None    
    ability_9: int | None
    stat: int | None
    stat_limit : int | None

class GacBattleData(BaseModel):
    battles: list[GacBattle]
    cc: DatacronCC | CC | None
    battlesCCin:  list[dict] | None  # recursion is not supported fully
    battlesCCout: list[dict] | None

class DCSLRow(BaseModel):
    id: int
    count: int
    long_desc: str

class DCSeasonList(BaseModel):
    season:int
    l3: list[DCSLRow]
    l6: list[DCSLRow]
    l9: list[DCSLRow]

#class PopularLeaders(BaseModel):
#    attackers: list[int]
#    defenders: list[int]

class PORow(BaseModel):
    id: int
    count: int
    name: str 
    opt1: str | None

class PrecalcObject(BaseModel):
    season: int
    item_type: str
    payload: list[PORow]



