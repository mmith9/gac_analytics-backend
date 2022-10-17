from app.data_classes import *
from app.db_objects import MyDb



def popular_leaders(my_db:MyDb )-> PopularLeaders:
    query = 'select count(*) as cnt_all, a1 from battles5v5 '
    query+= 'group by a1 order by cnt_all desc'

    cursor = my_db.cursor
    cursor.execute(query)
    rows = cursor.fetchall()

    attackers:list[int] = []
    for row in rows:
        attackers.append(row[1])
    
    query = 'select count(*) as cnt_all, d1 from battles5v5 '
    query += 'group by d1 order by cnt_all desc'

    cursor = my_db.cursor
    cursor.execute(query)
    rows = cursor.fetchall()

    defenders: list[int] = []
    for row in rows:
        defenders.append(row[1])

    return {'attackers':attackers, 'defenders':defenders}
