# -*- coding: utf-8 -*-

import pymysql
import logging
import configparser
import os

logger = logging.getLogger('app')


class connect():
    def __init__(self):
        ''' init mysql connection '''
        this_path = os.path.abspath(os.path.dirname(__file__))
        config_file = os.path.join(this_path, '../config/config.cfg')
        config = configparser.ConfigParser()
        config.read(config_file)
        dbConfig = config['database']
        db_host = dbConfig['DB_HOST']
        db_user = dbConfig['DB_USER']
        db_pass = dbConfig['DB_PASS']
        db_name = dbConfig['DB_NAME']
        self._connect = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        self._cursor = self._connect.cursor()

    def close(self):
        self._connect.close()

    def insert(self, sql, value):
        try:
            self._cursor.executemany(sql, value)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()
            logger.error(e)
            raise

    def update(self, sql, value):
        try:
            self._cursor.execute(sql, value)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()
            logger.error(e)
            raise

    def query(self, sql):
        try:
            result = ''
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise
        return result
