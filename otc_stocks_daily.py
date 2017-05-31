# -*- coding: utf-8 -*-

import datetime
import argparse
import logging
import libs.system
import libs.twcrawler
import libs.stockservice
import time

logger = logging.getLogger('app')


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

    # set logger
    libs.system.set_logger()
    # get headers
    headers = libs.system.get_headers()
    # update urllib proxy ip
    libs.system.update_urllib_proxy()

    # crawler
    otc = libs.twcrawler.OtcCrawler(headers)
    while 1 == 1:
        crawler_status, crawler_data = otc.get_every_stock_info(dCrawler)
        if crawler_status == 1:
            break
        if crawler_status == 2:
            libs.system.update_proxy_file()
            libs.system.update_urllib_proxy()
        time.sleep(10)

    if crawler_data['iTotalRecords'] == 0:
        return

    otc_stock_data = libs.stockservice.get_otc_stock_data(crawler_data)

    crawler_day = '{0}/{1:02d}/{2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
    if libs.stockservice.check_crawler_day_data_exist(crawler_day):
        libs.stockservice.insert_or_update_otc_stock_data(otc_stock_data)
        logger.info('Updating data .....')
    else:
        libs.stockservice.insert_otc_stock_data(otc_stock_data)
        logger.info('Inserting data .....')


if __name__ == '__main__':
    main()
