import json
from fastapi import Body, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware


from app.data_classes import *
from app.data_types import *
from app.db_objects import MyDb
from app.fetch_gac_data import *
from app.fetch_units_dict import *

from pprint import PrettyPrinter

import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

pp = PrettyPrinter()
app = FastAPI()
my_db = MyDb()
my_db.connect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.2.205:3000"],
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'DELETE', 'OPTIONS'],
    allow_headers=['Authorization',  'Content-Type'],
)


######
##  
#

@app.get("/", tags=["root"])
async def read_root():
    print('get / path')
    return 'A root dir'

@app.get("/characters")
async def characters_route() -> list[Unit]:
    print('@app.get("/characters")')
    units = fetch_units_dict(my_db)
    return units

@app.get("/gac_events")
async def read_events() -> dict:
    print('@app.get("/gac_events")')
    query ='select swgohgg_gac_season, swgohgg_gac_num, cg_territory_map_id '
    query+='from gac_events '
    
    cursor=my_db.cursor #TODO
    cursor.execute(query)
    last_row=0
    rows = cursor.fetchall()
    gac_season_list=[]
    for row in rows:
        if last_row != row[0]:
            last_row = row[0]
            next_season = {
                'type':row[2],
                'season':row[0],
                'rounds':[row[1]]
            }
            gac_season_list.append(next_season)
        else:
            next_season['rounds'].append(row[1])
    
    return gac_season_list

@app.post("/fetch_gac_data", status_code=200, response_model=GacBattleData)
async def fetch_gac_data_route(*, response: Response ,request: Request ,gac_request: GacDataRequest) -> dict:
    print(
        '@app.post("/fetch_gac_data", status_code=200, response_model=GacBattle)')

    #validation = fetch_gac_data_validate(data)
    data = fetch_gac_data(gac_request, my_db)

    pp.pprint(data)

    return data
   