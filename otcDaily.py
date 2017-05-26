# -*- coding: utf-8 -*-

import datetime
import argparse
import os
import logging
import libs.common
import libs.twcrawler
import libs.stockservice

logger = logging.getLogger('app')


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
    this_path = os.path.abspath(os.path.dirname(__file__))
    proxy_file = os.path.join(this_path, "config/proxy")
    log_file = os.path.join(this_path, "logs/app.log")

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
    crawler_data = otc.get_every_stock_info(dCrawler)
    if crawler_data['iTotalRecords'] == 0:
        return

    crawler_day = '{0}/{1:02d}/{2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
    if libs.stockservice.check_crawler_day_data_exist(crawler_day):
        print('have data')
    else:
        libs.stockservice.insert_otc_data(crawler_data)
        print('dont have data')


if __name__ == '__main__':
    main()
