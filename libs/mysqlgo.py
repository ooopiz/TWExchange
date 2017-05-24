# -*- coding: utf-8 -*-

import pymysql


class connect():
    def __init__(self, db_host, db_user, db_pass, db_name):
        ''' init mysql connection '''
        self._connect = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        self._cursor = self._connect.cursor()

    def close(self):
        self._connect.close()

    def execute(self, sql):
        try:
            self._cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()
            print(e)

    def executemany(self, sql, value):
        try:
            self._cursor.executemany(sql, value)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()
            print(e)

    def getSql_insert_otc_tmp():
        return "INSERT INTO otc_data(trade_date, \
               stock_no, close_price, diff_price, open_price, \
               top_price, down_price, total_volume, trade_price, trade_count, \
               last_buy_price, last_sell_price, issued_volume, next_top_price, \
               next_down_price) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
