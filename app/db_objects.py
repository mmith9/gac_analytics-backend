import os
import sys
import mysql.connector

import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

mysql_password = 'swgoh123'
mysql_user = 'swgoh'
mysql_host = '192.168.2.119'

class MyDb:
    def __init__(self) -> None:
        self.cursor: mysql.connector.cursor.MySQLCursor
        self.connection: mysql.connector.connection.MySQLConnection
        self.info = {}

    def connect(self):
        print('def connect(self):')
        mysql_database_name = "swgoh_gac"

        try:
            self.connection = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database=mysql_database_name
            )
            self.cursor = self.connection.cursor()
            
            logger.debug('connected to db')
        except mysql.connector.Error as err:
            
            logger.critical('Connection to db failed')
            logger.critical(err)


