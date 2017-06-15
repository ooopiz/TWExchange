# -*- coding: utf-8 -*-

import datetime
import argparse
import logging
import libs.system
import libs.twcrawler
import libs.stockservice

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

    date_str = '{0}/{1:02d}/{2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
    logger.info('Starting crawler ' + date_str)
    crawler_status, crawler_detail = otc.get_otc_dayily_close(dCrawler)

    if crawler_status == 0:
        logger.warning('Please Check date in range')
        return

    if len(crawler_detail) == 0:
        logger.info('No data in' + date_str)
        return

    if libs.stockservice.check_crawler_day_data_exist(dCrawler):
        libs.stockservice.insert_or_update_otc_stock_data(crawler_detail)
        logger.info('Updating data .....')
    else:
        libs.stockservice.insert_otc_stock_data(crawler_detail)
    # libs.system.update_proxy_file()
    # libs.system.update_urllib_proxy()

    # required field
    # 股票代號
    # 收盤價
    # 開盤價
    # 盤中最高價
    # 盤中最低價
    # 成交股數
    # 成交金額
    # 成交筆數
    # 最後買價
    # 最後賣價
    # 發行股數
    # 次日漲停價
    # 次日跌停價


if __name__ == '__main__':
    main()
