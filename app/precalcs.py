from app.db_objects import MyDb
from app.data_classes import *
from app.AllDatacronStats import AllDatacronStats
import mysql.connector
import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def precalcs(mydb:MyDb, season:int, item_type:str, leader:int) -> PrecalcObject:
    cursor = mydb.cursor
    data : PrecalcObject = {'season':season, 'item_type':item_type, 'payload':[]}


    if item_type in ['att_lead', 'def_lead']:
        # obsolete
        # query = 'select cg_territory_map_id from gac_events where swgohgg_gac_season = %s'
        # cursor.execute(query,(season,))
        # rows = cursor.fetchall()
        # map_id = rows[0][0]
        # if map_id.find('5v5')>=0:
        #     gac_type = '5v5'
        # elif map_id.find('3v3') >= 0:
        #     gac_type = '3v3'
        # else:
        #     logger.critical('unknown gac type %s', map_id)

        query = '''
            select unit_id, count from prc_units
            where season = %s and side = %s and leader is null
        '''
        side = item_type[0]
        logger.debug('query %s', query)
        logger.debug('params %s %s',season, side)
        cursor.execute(query, (season, side))

        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id':row[0], 'count':row[1]}
            data['payload'].append(data_row)
        
        return data

    if item_type in ['att_units_per_lead', 'def_units_per_lead'] :
        query = '''
            select unit_id, count from prc_units
            where season = %s and side = %s and leader = %s
        '''

        side = item_type[0]
        logger.debug('query %s', query)
        logger.debug('params %s %s',season, side)
        cursor.execute(query, (season, side, leader))

        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id':row[0], 'count':row[1]}
            data['payload'].append(data_row)
        
        return data

    
    if item_type in ['dc_ability_3', 'dc_ability_6', 'dc_ability_9']:
        dc_ab_level = int(item_type[-1])
        query='''
        select dc_mc_id, count, name from prc_dc_abilities
        where season = %s and ab_level=%s
        '''
        cursor.execute(query, (season, dc_ab_level))
        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id': row[0], 'count': row[1], 'name': row[2]}
            data['payload'].append(data_row)
        return data

    if item_type in ['dc_all_stats']:
        query='''
        select dc_stat_num, count, name, max_value from prc_dc_stats 
        where season = %s order by count desc
        '''

        cursor.execute(query, (season,))
        rows = cursor.fetchall()
        for row in rows:
            data_row: PORow = {'id': row[0], 'count': row[1], 'name': row[2], 'max_value': row[3]}
            data['payload'].append(data_row)
        return data

      
    

    return False



def create_precalc_tables(mydb: MyDb) -> None:
    logger.debug('dropping old tables')

    query = 'drop table prc_zuo'
    try:
        mydb.cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        pass

    query = '''
        create table prc_zuo (
        id          int primary key auto_increment,
        count       int,
        zuo_id      int,
        name        text,
        season      int )'''

    mydb.cursor.execute(query)
    mydb.connection.commit()

    query = 'drop table prc_dc_abilities'
    try:
        mydb.cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        pass
    
    query = '''
        create table prc_dc_abilities (
        id          int primary key auto_increment,
        count       int,
        season      int,
        dc_mc_id    int,
        name        text,
        ab_level    int )'''
    mydb.cursor.execute(query)
    mydb.connection.commit()

    query = 'drop table prc_dc_stats'
    try:
        mydb.cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        pass

    query = '''
        create table prc_dc_stats (
        id          int primary key auto_increment,
        dc_stat_num int,
        count       int,
        season      int,
        name        text,
        max_value   float )'''
    mydb.cursor.execute(query)
    mydb.connection.commit()
    return

def populate_precalc_tables(mydb:MyDb) -> None:
    logger.debug('populating precalc tables')
    #populate_precalc_tables_units(mydb)
    # populate_precalc_tables_zuo(mydb)
    # populate_precalc_tables_datacrons_abilities(mydb)
    # populate_precalc_tables_datacrons_stats(mydb)

    logger.debug('done precalculating tables')
    return


def create_precalc_table_units(mydb: MyDb) -> None:
    logger.debug('dropping units table')
    query = 'drop table prc_units'
    try:
        mydb.cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        pass

    query = '''
        create table prc_units (
        id          int primary key auto_increment,
        unit_id     smallint,
        count       mediumint,
        season      smallint,
        side        char(1),
        leader      smallint default null
        )'''
    mydb.cursor.execute(query)
    mydb.connection.commit()

def populate_precalc_tables_units(mydb: MyDb) -> None:
    create_precalc_table_units(mydb)
    query ='''
        insert into prc_units 
            (unit_id, count, season, side)
        
        select 
            battlesv2.a1,
            count(*) as cnt_all, 
            swgohgg_gac_season as season,
            'a'
        from
            gac_events ge
            inner join battlesv2 on(swgohgg_gac_num=bt_gac_num)
            where battlesv2.attempt = 1
            group by season, battlesv2.a1
            order by cnt_all desc'''
    logger.debug('populating prc_units')
    mydb.cursor.execute(query)
    #logger.debug('query %s', query)

    for sub in [('.a1', '.d1'), ("'a'", "'d'")]:
            query = query.replace(sub[0], sub[1])
    logger.debug('populating prc_units')
    #logger.debug('query %s', query)
    mydb.cursor.execute(query)
    mydb.connection.commit()
   
    logger.debug('populating prc_units part2')
    query = '''
        insert into prc_units
            (unit_id, count, season, side, leader)
        
        select
            ud.unit_id as unit,
            count(*) as cnt,
            swgohgg_gac_season as season,
            'a' as side,
            bv2.a1 as leader
        from            
            battlesv2 bv2
            inner join unit_dict ud on (ud.unit_id in (bv2.a2, bv2.a3, bv2.a4, bv2.a5))
            inner join gac_events ge on (ge.swgohgg_gac_num = bt_gac_num)
        where 
            attempt = 1 
        group by
            season, leader, unit
        order by
	        leader asc, cnt desc      
    '''
    mydb.cursor.execute(query)

    for sub in [('bv2.a', 'bv2.d'), ("'a'", "'d'")]:
        query = query.replace(sub[0], sub[1])
    logger.debug('populating prc_units part2')
    mydb.cursor.execute(query)
    mydb.connection.commit()



def populate_precalc_tables_zuo(mydb: MyDb) -> None:
    query = 'truncate prc_zuo'
    mydb.cursor.execute(query)
    query = '''
        insert into prc_zuo 
            (zuo_id, count, season, name)
        select 
            zuo_id,
            count(*) as cnt_all,
            swgohgg_gac_season as season,
            zuo_string as name

        from
            gac_events ge
            inner join zuo_bundle zb on(swgohgg_gac_num=zuo_gac_num)
            inner join zuo_dict zd on(zd.zuo_id = zb.zuo_dict_id)
            group by season, zd.zuo_id
            order by cnt_all desc '''
    logger.debug('populating prc_zuo')
    mydb.cursor.execute(query)


def populate_precalc_tables_datacrons_abilities(mydb: MyDb) -> None:
    query = 'truncate prc_dc_abilities'
    mydb.cursor.execute(query)

    query = '''
        insert into prc_dc_abilities 
            (dc_mc_id, count, season, name, ab_level)
        select
            dc_mc_id,
            count(*) as cnt_all,
            swgohgg_gac_season as season,            
            mc_string as name,
            3 as dc_ab_lv
        from
            gac_events ge
            inner join battlesv2 btl on (btl.bt_gac_num = ge.swgohgg_gac_num )
            inner join datacronsv2 dcs on (dcs.dc_id = btl.attacker_dc_id)
            inner join dc_mechanics_dict dmd on (dcs.dc_ability_3 = dmd.dc_mc_id)
            group by season, dc_mc_id
            order by cnt_all desc
            '''
    logger.debug('populating prc_dc_abilities')
    mydb.cursor.execute(query) 
    for subs in [
        [('3 as dc_ab_lv', '6 as dc_ab_lv'), 
            ("dcs.dc_ability_3 = dmd.dc_mc_id", "dcs.dc_ability_6 = dmd.dc_mc_id")],

        [('6 as dc_ab_lv', '9 as dc_ab_lv'),
            ("dcs.dc_ability_6 = dmd.dc_mc_id", "dcs.dc_ability_9 = dmd.dc_mc_id")]]:

        for sub in subs:
            query = query.replace(sub[0], sub[1])
        logger.debug('populating prc_dc_abilities')
        mydb.cursor.execute(query)
    
    mydb.connection.commit()


def populate_precalc_tables_datacrons_stats(mydb: MyDb) -> None:
    query = 'truncate prc_dc_stats'
    mydb.cursor.execute(query)

    all_stats = AllDatacronStats()

    for stat_num, props in all_stats.stats.items():
        stat_name = props['name']
        stat_column_name='dc_stat_' + str(stat_num)

        query = f'''
            insert into prc_dc_stats
                (dc_stat_num, count, season, name, max_value)
            select
                {stat_num} as stat_num,
                count(*) as cnt_all,
                swgohgg_gac_season as season,            
                '{stat_name}' as stat_name,
                max(dcs.{stat_column_name})

            from
                gac_events ge
                inner join battlesv2 btl on (btl.bt_gac_num = ge.swgohgg_gac_num )
                inner join datacronsv2 dcs on (dcs.dc_id = btl.attacker_dc_id)
                where dcs.{stat_column_name} is not null
                group by season
                order by cnt_all desc
                '''

        logger.debug('populating prc_dc_stats for: %s', stat_num)
        mydb.cursor.execute(query)
    logger.debug('commiting dc stats')
    mydb.connection.commit()
