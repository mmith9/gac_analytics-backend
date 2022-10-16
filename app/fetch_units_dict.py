import json
import mysql.connector
import requests

from app.data_classes import Unit
from app.db_objects import MyDb

import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


def fetch_units_dict(my_db:MyDb):
    print('def fetch_units_dict(my_db:MyDb):')

    query = 'select base_id from unit_dict where image_url is null'

    cursor = my_db.cursor
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        update_units_dict(rows, my_db)

    query ='select unit_id, base_id, image_url, name from unit_dict'
    cursor.execute(query)
    rows = cursor.fetchall()

    units:list[Unit] = []
    for row in rows:
        units.append({
            'unit_id':row[0],
            'base_id':row[1],
            'image_url':row[2],
            'name':row[3]
        })

    return units


def update_units_dict(rows, my_db:MyDb) -> None:
    
    url = 'http://api.swgoh.gg/characters/'
    try:
        response = requests.get(url)
    except mysql.connector.Error:
        logger.critical(
            'failed to update images from api.swgoh.gg/characters')
        return

    try:
        swgoh_units = json.loads(response.text)
    except UnicodeDecodeError:
        logger.critical('failed to decode json object')
        return
    
    query = 'update unit_dict set image_url= %s where base_id =%s'
    for row in rows:
        base_id = row[0]
        for swgoh_unit in swgoh_units:
            if base_id == swgoh_unit['base_id']:
                my_db.cursor.execute(query, (swgoh_unit['image'], base_id))
                break
    my_db.connection.commit()

                



    

        

