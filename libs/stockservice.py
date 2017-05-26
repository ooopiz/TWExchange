# -*- coding: utf-8 -*-

import logging
import libs.mysqlgo

logger = logging.getLogger('app')


def check_crawler_day_data_exist(str_date):
    sql = 'select count(*) from otc_data where trade_date = "%s"' % str_date
    dbconnect = libs.mysqlgo.connect()
    data = dbconnect.execute(sql)
    if data[0][0] > 0:
        return True
    else:
        return False


def insert_otc_data(crawler_data):
    sql = 'INSERT INTO otc_data(trade_date, \
           stock_no, close_price, diff_price, open_price, \
           top_price, down_price, total_volume, trade_price, trade_count, \
           last_buy_price, last_sell_price, issued_volume, next_top_price, \
           next_down_price) \
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    report_date = crawler_data['reportDate']
    split_date = report_date.split('/')
    trade_date = str(int(split_date[0]) + 1911) + '/' + split_date[1] + '/' + split_date[2]
    trade_detail = []
    for value in crawler_data['aaData']:
        trade_detail.append((trade_date,
                            value[0].strip(),
                            value[2].strip(),
                            value[3].strip(),
                            value[4].strip(),
                            value[5].strip(),
                            value[6].strip(),
                            value[8].strip().replace(',', ''),
                            value[9].strip().replace(',', ''),
                            value[10].strip().replace(',', ''),
                            value[11].strip(),
                            value[12].strip(),
                            value[13].strip().replace(',', ''),
                            value[15].strip(),
                            value[16].strip()))
    dbconnect = libs.mysqlgo.connect()
    dbconnect.executemany(sql, trade_detail)
