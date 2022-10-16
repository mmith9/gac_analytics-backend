#print('fetch_gac_data.py :', __name__)


from app.data_classes import *
import mysql.connector
import logging
import logging.config
import sqlalchemy

from app.db_objects import MyDb
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def fetch_gac_data_validate(data):
    return True

def fetch_gac_data(gac_request: GacDataRequest, my_db:MyDb)-> list[GacBattle] :
    #logger.debug('entered fetch_gac_data')
    #print(gac_request)
    if gac_request.season.type == '3v3':
        battles_table = 'battles3v3 '
        unit_limit = 3
        all_columns = 'd1, d2, d3, a1, a2, a3 '
        include_def= ' in (d2, d3) '
        include_att= ' in (a2, a3) '
    else:
        battles_table = 'battles5v5 '
        unit_limit = 5
        all_columns = 'd1, d2, d3, d4, d5, a1, a2, a3, a4, a5 '
        include_def = ' in (d2, d3, d4, d5) '
        include_att = ' in (a2, a3, a4, a5) '

    if 'cutoff' in gac_request:
        cutoff = gac_request.cutoff
    else:
        cutoff = 10

    query = 'select '
    query+= 'round(100*sum(case when banners > 0 then 1 end)/count(*), 2) as win_percent, '
    query+= 'count(*) as count_all, '
    query+= 'count(case when banners > 0 then 1 end) as count_win, '
    query+= 'round(avg(case when banners > 0 then banners end), 2) as avg_banners, '
    query+= all_columns
    query+= 'from ' + battles_table
    query+= 'where '
    query+= 'd1 = ' + str(gac_request.defenders.leader.unit_id)

    for unit in gac_request.defenders.members[1:]:
        query+= ' and ' + str(unit.unit_id) + include_def

    if gac_request.attackers:
        query += ' and a1 = ' + str(gac_request.attackers.leader.unit_id)
        for unit in gac_request.attackers.members[1:]:
            query += ' and ' + str(unit.unit_id) + include_att
    
    query+= ' group by ' + all_columns
    query+= ' having count_all > ' + str(cutoff) + ' '
    query+= ' order by win_percent desc'

    logger.debug('\nprepared query: \n%s', query)
    
    my_db.cursor.execute(query)
    rows = my_db.cursor.fetchall()
    data:GacBattleData={
        'battles':[]
    }

    for row in rows:
        win_percent = none_to_0(row[0])
        count_all = none_to_0(row[1])
        count_win = none_to_0(row[2])
        avg_banners = none_to_0(row[3])
        defs =[]
        attk =[]
        for x in range(4, 4+unit_limit):
            if row[x] !=0:
                defs.append(row[x])
        for x in range(4+unit_limit, 4+unit_limit*2):
            if row[x] != 0:
                attk.append(row[x])
        
        gac_battle:GacBattle={
            'attackers':attk,
            'defenders':defs,
            'wins':count_win,
            'losses':count_all-count_win,
            'avg_banners':avg_banners,
            'win_percent':win_percent
        }
        data['battles'].append(gac_battle)
    
    return data

def none_to_0(x):
    if not x:
        return 0
    else:
        return x