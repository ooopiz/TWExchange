# -*- coding: utf-8 -*-

import pymysql


class connect():
    def __init__(self, db_host, db_user, db_pass, db_name):
        ''' init db connection '''
        self._dbconnect = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        self._cursor = self._dbconnect.cursor()

    def dbClose(self):
        self._dbconnect.close()

    def insertData(self, value):
        ''' insert crawler data to db '''
        sql = "INSERT INTO otc_data_tmp(trade_date, \
               stock_no, close_price, diff_price, open_price, \
               top_price, down_price, total_volume, trade_price, trade_count, \
               last_buy_price, last_sell_price, issued_volume, next_top_price, \
               next_down_price) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            self._cursor.executemany(sql, value)
            self._dbconnect.commit()
        except Exception as e:
            self._dbconnect.rollback()
            print(e)


#    config = configparser.ConfigParser()
#    config.read('config')
#    dbConfig = config['database']
#    dbHost = dbConfig['DB_HOST']
#    dbUser = dbConfig['DB_USER']
#    dbPass = dbConfig['DB_PASS']
#    dbName = dbConfig['DB_NAME']
#    databasego = Databasego(dbHost, dbUser, dbPass, dbName)

#    handleCrawler(crawler, databasego, crawler_day)

#    databasego.dbClose
