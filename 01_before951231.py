# -*- coding: utf-8 -*-

import datetime
import os


def main():
    this_path = os.path.abspath(os.path.dirname(__file__))
    crawler_file = os.path.join(this_path, "otc_stocks_daily.py")

    start_date = datetime.datetime(2003, 8, 1)
    end_date = datetime.datetime(2006, 12, 31)

    dCrawler = start_date
    while start_date <= end_date:
        str_day = '{0} {1:02d} {2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
        command = 'python3 ' + crawler_file + ' ' + str_day
        os.system(command)
        dCrawler = dCrawler + datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
