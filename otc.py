# coding=utf-8

import urllib.request
import json
import pymysql
import configparser
import datetime
import time
import argparse


class Databasego():
    def __init__(self, db_host, db_user, db_pass, db_name):
        ''' init db connection '''
        self._dbconnect = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        self._cursor = self._dbconnect.cursor()

    def insertData(self, value):
        ''' insert crawler data to db '''
        sql = "INSERT INTO otc_data_tmp(trade_date, \
               stock_no, close_price, diff_price, open_price, \
               top_price, down_price, total_volume, trade_price, trade_count, \
               last_buy_price, last_sell_price, issued_volume, next_top_price, \
               next_down_price) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
               %s, %s, %s, %s, %s)"

        try:
            self._cursor.executemany(sql, value)
            self._dbconnect.commit()
        except Exception as e:
            self._dbconnect.rollback()
            print(e)

    def dbClose(self):
        self._dbconnect.close()


class Crawler():
    def _get_otc_data(self, date_str):
        ttime = str(int(time.time()*100))
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(date_str, ttime)
        res = urllib.request.urlopen(url)
        response = res.read().decode('utf-8')
        resJson = json.loads(response)
        c_tradeDate = resJson['reportDate']
        e_tradeDate = c_tradeDate.replace(c_tradeDate[0:3], str(int(c_tradeDate[0:3])+ 1911))
        '''
        aaData[0]  = 股票代號
        aaData[1]  = 股票名稱
        aaData[2]  = 收盤價
        aaData[3]  = 漲跌
        aaData[4]  = 開盤價
        aaData[5]  = 盤中最高
        aaData[6]  = 盤中最低
        aaData[7]  = 均價
        aaData[8]  = 成交股數
        aaData[9]  = 成交金額(元)
        aaData[10] = 成交筆數
        aaData[11] = 最後買價
        aaData[12] = 最後賣價
        aaData[13] = 發行股數
        aaData[14] = 次日參考價
        aaData[15] = 次日漲停價
        aaData[16] = 次日跌停價
        '''

        print('日期: ' + e_tradeDate + ',   筆數: ' + str(resJson['iTotalRecords']))
        resJson['reportDate'] = e_tradeDate  # 換成西元年
        return resJson


def handleCrawler(crawler, databasego, crawler_day):
    responseData = crawler._get_otc_data(crawler_day)

    # 沒資料就離開
    if responseData['iTotalRecords'] == 0:
        return

    tradeDetail = []
    for value in responseData['aaData']:
        tradeDetail.append((responseData['reportDate'],
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
                            value[16].strip()
                            ))

    databasego.insertData(tradeDetail)


def main():
    '''
    tse first day is 2004/02/11

    otc
    106/04/23 之後 http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=96/04/23&_=1495463910075
    '''

    # Get arguments
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*',
                        help='assigned day (format: YYYY MM DD), default is today')
    parser.add_argument('-b', '--back', action='store_true',
                        help='crawl back from assigned day until 2004/2/11')

    args = parser.parse_args()

    # Day only accept 0 or 3 arguments
    if len(args.day) == 0:
        crawlerD = datetime.datetime.today()
    elif len(args.day) == 3:
        crawlerD = datetime.datetime(args.day[0], args.day[1], args.day[2])
    else:
        parser.error('Date should be assigned with (YYYY MM DD) or none')
        return

    crawler_day = '{0}/{1:02d}/{2:02d}'.format(crawlerD.year - 1911, crawlerD.month, crawlerD.day)

    # new Crawler
    crawler = Crawler()

    # new Databasego
    config = configparser.ConfigParser()
    config.read('config')
    dbConfig = config['database']
    dbHost = dbConfig['DB_HOST']
    dbUser = dbConfig['DB_USER']
    dbPass = dbConfig['DB_PASS']
    dbName = dbConfig['DB_NAME']
    databasego = Databasego(dbHost, dbUser, dbPass, dbName)

    handleCrawler(crawler, databasego, crawler_day)

    databasego.dbClose


if __name__ == '__main__':
    main()
