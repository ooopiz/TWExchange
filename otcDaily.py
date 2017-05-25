# -*- coding: utf-8 -*-

import configparser
import datetime
import argparse
import os
import logging

import libs.common
import libs.twcrawler
import libs.mysqlgo


logger = logging.getLogger('app')


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
    logger.info('create proxy file ...')


def set_logger(log_path=''):
    if not log_path == '':
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(name)-3s - %(levelname)-8s] %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            handlers=[logging.FileHandler(log_path, 'a', 'utf-8')])

    formatter = logging.Formatter('%(asctime)s [%(levelname)-7s] : %(message)s')

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    applogger = logging.getLogger('app')
    applogger.addHandler(console)
    applogger.setLevel(logging.DEBUG)


def main():

    # Get arguments
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*',
                        help='assigned day (format: YYYY MM DD), default is today')

    args = parser.parse_args()

    # Day only accept 0 or 3 arguments
    if len(args.day) == 0:
        dCrawler = datetime.datetime.today()
    elif len(args.day) == 3:
        dCrawler = datetime.datetime(args.day[0], args.day[1], args.day[2])
    else:
        parser.error('Date should be assigned with (YYYY MM DD) or none')
        return

    # define absolute files path
    root_dir = os.path.dirname(os.path.realpath(__file__))
    proxy_file = root_dir + '/config/proxy'
    config_file = root_dir + '/config/config'
    log_file = root_dir + '/logs/app.log'

    # set logger
    set_logger(log_file)
    # get headers
    headers = libs.common.get_headers()
    # get and save proxy
    if not os.path.isfile(proxy_file):
        url = libs.common.get_gimmeproxy_url(headers)
        update_proxy_file(proxy_file, url)

    # update proxy
    proxy_url = get_proxyurl_from_file(proxy_file)
    libs.common.update_urllib_proxy(proxy_url)

    # crawler
    otc = libs.twcrawler.OtcCrawler(headers)
    otc.get_every_stock_info(dCrawler)

    config = configparser.ConfigParser()
    config.read(config_file)
    dbConfig = config['database']
    dbHost = dbConfig['DB_HOST']
    dbUser = dbConfig['DB_USER']
    dbPass = dbConfig['DB_PASS']
    dbName = dbConfig['DB_NAME']
    dbconnect = libs.mysqlgo.connect(dbHost, dbUser, dbPass, dbName)
    dbconnect.execute('select 1')
    dbconnect.close()


if __name__ == '__main__':
    main()
