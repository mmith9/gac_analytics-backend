import json
import mysql.connector
import requests

from app.data_classes import DictBundle, Zuo, DcMechanic, UnitStat, Unit, DcStat
from app.db_objects import MyDb

import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def fetch_dictionaries(my_db:MyDb) -> DictBundle:
    data:DictBundle = {
        'unit_dict': fetch_units_dict(my_db),
        'zuo_dict': fetch_zuo_dict(my_db),
        'dc_mc_dict': fetch_dc_mc_dict(my_db),
        'unit_stat_dict': fetch_unit_stat_dict(),
        'dc_stat_dict': fetch_dc_stat_dict(),
    }
    return data

def fetch_zuo_dict(my_db:MyDb) -> list[Zuo]:
    zuo_dict:list[Zuo] = []
    query = 'select zuo_id, zuo_string from zuo_dict'
    my_db.cursor.execute(query)
    rows = my_db.cursor.fetchall()
    for row in rows:        
        zuo_dict.append(({'zuo_id':row[0], 'zuo_name':row[1]}))
    return zuo_dict


def fetch_dc_mc_dict(my_db: MyDb) -> list[DcMechanic]:
    dc_mc_dict: list[DcMechanic] = []
    query = 'select dc_mc_id, mc_string from dc_mechanics_dict'
    my_db.cursor.execute(query)
    rows = my_db.cursor.fetchall()
    for row in rows:
        dc_mc_dict.append(({'zuo_id': row[0], 'zuo_name': row[1]}))
    return dc_mc_dict

def fetch_units_dict(my_db:MyDb) -> list[Unit]:
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

                
class AllUnitStats:
    def __init__(self) -> None:
        self.stats = {}
        self.stats[1] = 'health'
        self.stats[5] = 'speed'
        self.stats[6] = 'phys_dmg'
        self.stats[7] = 'special_dmg'
        self.stats[8] = 'armor'
        self.stats[14] = 'phys_crit'
        self.stats[15] = 'special_crit'
        self.stats[16] = 'crit_dmg'
        self.stats[17] = 'potency'
        self.stats[18] = 'tenacity'
        self.stats[28] = 'protection'
        self.stats[39] = 'phys_ca'


def all_unit_stats():
    stats = AllUnitStats()
    data = stats.stats
    return data

def fetch_unit_stat_dict() -> list[UnitStat]:
    stats = AllUnitStats()
    us_dict: list[UnitStat]=[]
    for key in stats.stats:
        us_dict.append({'stat_id':str(key), 'stat_name':stats.stats[key]})
    return us_dict


class AllDatacronStats:
    def __init__(self) -> None:
        self.stats = {}
        self.stats[16] = {'name': 'crit dmg %', 'type': 'float'}  # 16 (cd?)
        self.stats[17] = {'name': 'potency', 'type': 'float'}  # 17 (potency?)
        self.stats[18] = {'name': 'tenacity',
                          'type': 'float'}  # 18 (tenacity?)
        self.stats[19] = {'name': 'dodge', 'type': 'float'}  # 19 dodge
        self.stats[20] = {'name': 'deflection',
                          'type': 'float'}  # 20 deflection
        self.stats[21] = {'name': 'phys crit %',
                          'type': 'float'}  # 21 phys crit
        self.stats[22] = {'name': 'special crit %',
                          'type': 'float'}  # 22 special crit
        self.stats[23] = {'name': 'armor %', 'type': 'float'}  # 23 armor
        self.stats[24] = {'name': 'resistance %',
                          'type': 'float'}  # 24 resistance
        self.stats[25] = {'name': 'armor penetration %',
                          'type': 'float'}  # 25 arpen
        self.stats[26] = {'name': 'resistance pentration %',
                          'type': 'float'}  # 26 respen
        self.stats[27] = {'name': 'hp steal %',
                          'type': 'float'}  # 27 (hp steal?)
        self.stats[31] = {'name': 'phys dmg %',
                          'type': 'float'}  # 31 physical damage
        self.stats[32] = {'name': 'special dmg %',
                          'type': 'float'}  # 32 special damage
        self.stats[33] = {'name': 'phys acc %',
                          'type': 'float'}  # 33 phys accuracy
        self.stats[34] = {'name': 'special acc %',
                          'type': 'float'}  # 34 special accuracy
        self.stats[35] = {'name': 'phys ca %', 'type': 'float'}  # 35 phys ca
        self.stats[36] = {'name': 'special ca %',
                          'type': 'float'}  # 36 special ca
        self.stats[55] = {'name': 'hp %', 'type': 'float'}  # 55 (hp?)
        self.stats[56] = {'name': 'prot %', 'type': 'float'}  # 56 (prot?)
        self.ability_indices = (3, 6, 9)
        self.stat_indices = [x for x in self.stats]

def fetch_dc_stat_dict() -> list[DcStat]:
    stats = AllDatacronStats()
    ds_dict: list[DcStat] = []
    for key in stats.stats:
        ds_dict.append({'stat_id':key, 'stat_name': stats.stats[key]['name']})
    return ds_dict



        

