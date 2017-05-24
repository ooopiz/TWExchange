# coding=utf-8

import pymysql
import configparser
import datetime
import argparse
import os

import libs.common
import libs.twcrawler


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


def get_proxyurl_from_file(proxy_file):
    r_file = open(proxy_file, 'r')
    proxy_url = r_file.read()
    proxy_url = proxy_url.strip()
    r_file.close()
    return proxy_url


def update_proxy_file(proxy_file_path, proxy_url):
    w_file = open(proxy_file_path, 'w')
    w_file.write(proxy_url)
    w_file.close()
    print('create proxy file ...')


def main():
    # get headers
    headers = libs.common.get_headers()

    root_dir = os.path.dirname(os.path.realpath(__file__))
    proxy_file = root_dir + '/config/proxy'
    if not os.path.isfile(proxy_file):
        url = libs.common.get_gimmeproxy_url(headers)
        update_proxy_file(proxy_file, url)

    proxy_url = get_proxyurl_from_file(proxy_file)
    libs.common.update_urllib_proxy(proxy_url)

    # Get arguments
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*',
                        help='assigned day (format: YYYY MM DD), default is today')

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

    otc = libs.twcrawler.OtcCrawler(headers)
    abc = otc.get_otc_data(crawler_day)
    print(abc)

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


if __name__ == '__main__':
    main()
