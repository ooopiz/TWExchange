# -*- coding: utf-8 -*-

import logging
import libs.mysqlgo

logger = logging.getLogger('app')


def check_crawler_day_data_exist(dCrawler):
    date_str = '{0}/{1:02d}/{2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
    sql = 'select count(*) from otc_stocks where trade_date = "%s"' % date_str
    dbconnect = libs.mysqlgo.connect()
    data = dbconnect.query(sql)
    if data[0][0] > 0:
        return True
    else:
        return False


def insert_otc_stock_data(otc_stock_data):
    sql = 'INSERT INTO otc_stocks(trade_date, \
           stock_no, close_price, open_price, \
           top_price, down_price, total_volume, trade_price, trade_count, \
           last_buy_price, last_sell_price, issued_volume, next_top_price, \
           next_down_price) \
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    dbconnect = libs.mysqlgo.connect()
    dbconnect.insert(sql, otc_stock_data)


def update_otc_stock_data(otc_stock_data):
    sql = 'UPDATE otc_stocks \
              SET close_price  = %s, \
                  open_price   = %s, \
                  top_price    = %s, \
                  down_price   = %s, \
                  total_volume = %s, \
                  trade_price  = %s, \
                  trade_count  = %s, \
                  last_buy_price  = %s, \
                  last_sell_price = %s, \
                  issued_volume   = %s, \
                  next_top_price  = %s, \
                  next_down_price = %s \
            WHERE trade_date = %s and stock_no = %s'
    dbconnect = libs.mysqlgo.connect()
    dbconnect.update(sql, otc_stock_data)


def insert_or_update_otc_stock_data(otc_stock_data):
    dbconnect = libs.mysqlgo.connect()

    for value in otc_stock_data:
        sql = 'select count(*) from otc_stocks where trade_date = "%s" and stock_no = "%s"' % \
                (value[0], value[1])
        data = dbconnect.query(sql)
        if data[0][0] > 0:
            update_data = [value[2],
                           value[3],
                           value[4],
                           value[5],
                           value[6],
                           value[7],
                           value[8],
                           value[9],
                           value[10],
                           value[11],
                           value[12],
                           value[13],
                           value[0],
                           value[1]]
            update_otc_stock_data(update_data)
        else:
            insert_data = []
            insert_data.append(value)
            insert_otc_stock_data(insert_data)
