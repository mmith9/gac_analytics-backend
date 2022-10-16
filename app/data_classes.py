from pydantic import BaseModel

class Unit(BaseModel):
    name:str
    image_url:str
    unit_id:str
    base_id:str
    
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
    defenders: Team 
    constraints: list[CC] | None
    cutoff: int | None

class GacBattleData(BaseModel):
    battles: list[GacBattle]
    cc: CC | None
    battlesCCin:  list[dict] | None  # recursion is not supported fully
    battlesCCout: list[dict] | None








