from app.data_classes import *
from app.db_objects import MyDb


def dcs_per_season(season: int, my_db:MyDb) -> DCSeasonList:
    cursor = my_db.cursor
    query = 'select swgohgg_gac_num from gac_events '
    query+= 'where swgohgg_gac_season = %s'
    cursor.execute(query, (season,))
    rows = cursor.fetchall()
    if not rows:
        return None
    
    gac_nums=''
    for row in rows:
        gac_nums+= str(row[0]) + ','
    gac_nums = gac_nums[:-1] #trailing coma
    
    season_list:DCSeasonList = {
        season:season,
        'l3':[],
        'l6':[],
        'l9':[]
    }
    
    for level in ['3', '6', '9']:
        query = 'select dc_mc_id, count(*) as cnt_all, mc_string '
        query+= 'from dc_mechanics_dict inner join datacrons on(dc_mc_id=dc_ability_' + level + ') '
        query+= 'where dc_gac_num in (' + gac_nums +') '
        query+= 'group by dc_mc_id order by cnt_all desc'

        l_level = 'l'+level
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:        
            entry: DCSLRow = {'id': row[0], 'count': row[1], 'long_desc': row[2]}
            season_list[l_level].append(entry)

    return season_list

        


            