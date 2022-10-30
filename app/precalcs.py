from app.db_objects import MyDb
from app.data_classes import *
import mysql.connector
import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def precalcs(mydb:MyDb, season:int, item_type:str) -> PrecalcObject:
    cursor = mydb.cursor
    data : PrecalcObject = {'season':season, 'item_type':item_type, 'payload':[]}
    if item_type in ['att_lead', 'def_lead']:
        query = 'select cg_territory_map_id from gac_events where swgohgg_gac_season = %s'
        cursor.execute(query,(season,))
        rows = cursor.fetchall()
        map_id = rows[0][0]
        if map_id.find('5v5')>=0:
            gac_type = '5v5'
        elif map_id.find('3v3') >= 0:
            gac_type = '3v3'
        else:
            logger.critical('unknown gac type %s', map_id)

        query = '''
            select unit_id, lead_count, name from prc_units
            where season = %s and side = %s
        '''
        side = item_type[0]
        cursor.execute(query, (season, side))
        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id':row[0], 'count':row[1], 'name':row[2]}
            data['payload'].append(data_row)
        
        return data
    
    if item_type in ['dc_ability_3', 'dc_ability_6', 'dc_ability_9']:
        dc_ab_level = int(item_type[-1])
        query='''
        select dc_mc_id, count, name from prc_dc 
        where season = %s and ab_level=%s
        '''
        cursor.execute(query, (season, dc_ab_level))
        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id': row[0], 'count': row[1], 'name': row[2]}
            data['payload'].append(data_row)
        return data

    if item_type in []:
        #TODO
        pass




        
    

    return False

def create_precalc_tables(mydb:MyDb) -> None:
    # query = 'drop table prc_units'
    # try:
    #     mydb.cursor.execute(query)
    # except mysql.connector.errors.ProgrammingError:
    #     pass

    # query = '''
    #     create table prc_units (
    #     id          int primary key auto_increment,
    #     unit_id     int,
    #     lead_count  int,
    #     season      int,
    #     base_id     varchar(50),
    #     name        text,
    #     image_url   text,
    #     side        char(1) )'''
    # mydb.cursor.execute(query)
    # mydb.connection.commit()

    # query = 'drop table prc_zuo'
    # try:
    #     mydb.cursor.execute(query)
    # except mysql.connector.errors.ProgrammingError:
    #     pass

    # query = '''
    #     create table prc_zuo (
    #     id          int primary key auto_increment,
    #     count       int,
    #     zuo_id      int,
    #     name        text,
    #     season      int )'''

    # mydb.cursor.execute(query)
    # mydb.connection.commit()

    query = 'drop table prc_dc'
    try:
        mydb.cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        pass
    
    query = '''
        create table prc_dc (
        id          int primary key auto_increment,
        count       int,
        season      int,
        dc_mc_id    int,
        name        text,
        ab_level    int )'''
    mydb.cursor.execute(query)
    mydb.connection.commit()
    return


def populate_precalc_tables(mydb:MyDb) -> None:
    # query = 'truncate prc_units'
    # mydb.cursor.execute(query)

    # query ='''
    #     insert into prc_units 
    #         (unit_id, lead_count, season, base_id, name, image_url, side)
        
    #     select 
    #         ud.unit_id,
    #         count(*) as cnt_all, 
    #         swgohgg_gac_season as season,
    #         ud.base_id,
    #         ud.name, 
    #         ud.image_url,
    #         'a'
    #     from
    #         gac_events ge
    #         inner join battles5v5 b5v5 on(swgohgg_gac_num=bt_gac_num)
    #         inner join unit_dict ud on(ud.unit_id=b5v5.a1)
    #         group by season, b5v5.a1
    #         order by cnt_all desc'''
    # logger.debug('populating prc_units')
    # mydb.cursor.execute(query)

    # for subs in [
    #     [('5v5', '3v3')],
    #     [('.a1', '.d1'), ("'a'","'d'")],
    #     [('3v3','5v5')]
    #     ]:
    #     for sub in subs:
    #         query = query.replace(sub[0], sub[1])
    #     logger.debug('populating prc_units')
    #     mydb.cursor.execute(query)
    # mydb.connection.commit()

    # query = 'truncate prc_zuo'
    # mydb.cursor.execute(query)
    # query = '''
    #     insert into prc_zuo 
    #         (zuo_id, count, season, name)
    #     select 
    #         zuo_id,
    #         count(*) as cnt_all,
    #         swgohgg_gac_season as season,
    #         zuo_string as name

    #     from
    #         gac_events ge
    #         inner join zuo_bundle zb on(swgohgg_gac_num=zuo_gac_num)
    #         inner join zuo_dict zd on(zd.zuo_id = zb.zuo_dict_id)
    #         group by season, zd.zuo_id
    #         order by cnt_all desc '''
    # logger.debug('populating prc_zuo')
    # mydb.cursor.execute(query)

    # query = 'truncate prc_dc'
    # mydb.cursor.execute(query)

    query = '''
        insert into prc_dc 
            (dc_mc_id, count, season, name, ab_level)
        select
            dc_mc_id,
            count(*) as cnt_all,
            swgohgg_gac_season as season,            
            mc_string as name,
            3 as dc_ab_lv
        from
            gac_events ge
            inner join datacrons dcs on (swgohgg_gac_num = dc_gac_num)
            inner join dc_mechanics_dict dmd on (dc_ability_3 = dc_mc_id)
            group by season, dc_mc_id
            order by cnt_all desc
            '''
    logger.debug('populating prc_dc')
    mydb.cursor.execute(query) 
    for subs in [
        [('3 as dc_ab_lv', '6 as dc_ab_lv'), 
            ("dc_ability_3 = dc_mc_id", "dc_ability_6 = dc_mc_id")],

        [('6 as dc_ab_lv', '9 as dc_ab_lv'),
            ("dc_ability_6 = dc_mc_id", "dc_ability_9 = dc_mc_id")]]:

        for sub in subs:
            query = query.replace(sub[0], sub[1])
        logger.debug('populating prc_dc')
        mydb.cursor.execute(query)
    
    logger.debug('done precalculating tables')

    mydb.connection.commit()
    return
