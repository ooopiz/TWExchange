# -*- coding: utf-8 -*-

import datetime
import os
import time


def main():
    this_path = os.path.abspath(os.path.dirname(__file__))
    crawler_file = os.path.join(this_path, "otc_stocks_daily.py")

    start_date = datetime.datetime(2007, 4, 23)
    end_date = datetime.datetime.today()

    dCrawler = start_date
    while start_date <= end_date:
        str_day = '{0} {1:02d} {2:02d}'.format(dCrawler.year, dCrawler.month, dCrawler.day)
        command = 'python3 ' + crawler_file + ' ' + str_day
        os.system(command)
        dCrawler = dCrawler + datetime.timedelta(days=1)
        time.sleep(30)


if __name__ == '__main__':
    main()
