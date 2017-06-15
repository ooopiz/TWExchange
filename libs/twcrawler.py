# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import datetime
import logging
import socket
import bs4
import pandas

logger = logging.getLogger('app')


class OtcCrawler():
    def __init__(self, headers={}):
        self.headers = headers

    # ==========================================================================
    # 1.st
    # ==========================================================================
    def _get_before_951231(self, dCrwaler):
        ''' 92/08/01 ~ 95/12/31 '''
        url = 'http://hist.tpex.org.tw/Hist/STOCK/AFTERTRADING/DAILY_CLOSE_QUOTES/RSTA3104_{0}{1:02d}{2:02d}.HTML'
        request_url = url.format(dCrwaler.year - 1911, dCrwaler.month, dCrwaler.day)
        myRequest = urllib.request.Request(request_url, headers=self.headers)
        try:
            response = urllib.request.urlopen(myRequest, timeout=15)
            dom = response.read().decode('big5', 'ignore')
            return dom
        except socket.timeout:
            logger.warning('_get_stocks_before_951231 timeout ...')
            raise
        except Exception as e:
            logger.error(e)
            raise

    def _get_before_951231_clean(self, dom):
        ''' Clean data and return json '''
        soup = bs4.BeautifulSoup(dom, "lxml")
        table = pandas.read_html(str(soup.find_all('table')[0]))[0]
        # delete table head
        table = table.drop(table.columns[[0]], axis=0)
        # replace string
        table[7] = table[7].str.replace('♁', '')

        jsonstr = table.to_json(orient="records")
        json_data = json.loads(jsonstr)
        return json_data

    def _get_before_951231_filter(self, c_date, json_data):
        ''' Filter the required information, return list '''
        date_str = '{0}/{1:02d}/{2:02d}'.format(c_date.year, c_date.month, c_date.day)
        datalist = []
        for value in json_data:
            datalist.append((date_str,
                             value['0'], value['3'], value['6'], value['7'], value['9'],
                             value['10'], value['11'], value['12'], value['13'], value['14'],
                             value['15'], value['17'], value['18']))
        return datalist

    # ==========================================================================
    # 2.st
    # ==========================================================================

    # ==========================================================================
    # 3.st
    # ==========================================================================
    def _get_after_960423(self, dCrwaler):
        ''' after 96/04/23 '''
        #   reportDate:    日期
        #   reportTitle:
        #   iTotalRecords: 資料總筆數
        #   iTotalDisplayRecords: 資料總顯示筆數
        #   listNum:     上櫃家數
        #   totalAmount: 總成交金額(元)
        #   totalVolumn: 總成交股數
        #   totalCount:  總交易筆數
        #   mmData: []
        #   aaData: [股票代號 ,股票名稱 ,收盤價 ,漲跌 ,開盤價 ,盤中最高 ,盤中最低 ,均價 ,成交股數,
        #            成交金額(元) ,成交筆數 ,最後買價 ,最後賣價 ,發行股數 ,次日參考價 ,次日漲停價 ,次日跌停價]

        ttime = str(int(time.time()*100))
        date_str = '{0}/{1:02d}/{2:02d}'.format(dCrwaler.year - 1911, dCrwaler.month, dCrwaler.day)
        params = 'l=zh-tw&d={}&_={}'.format(date_str, ttime)
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?'
        request_url = url + params
        myRequest = urllib.request.Request(request_url, headers=self.headers)
        try:
            response = urllib.request.urlopen(myRequest, timeout=15)
            dom = response.read().decode('utf-8')
            return dom
        except socket.timeout:
            logger.warning('_get_stocks_after_960423 timeout ...')
            raise
        except Exception as e:
            logger.error(e)
            raise

    def _get_after_960423_filter(self, json_data):
        ''' Filter the required information, return list '''
        report_date = json_data['reportDate']
        split_date = report_date.split('/')
        trade_date = str(int(split_date[0]) + 1911) + '/' + split_date[1] + '/' + split_date[2]
        datalist = []
        for value in json_data['aaData']:
            if value[2].strip() == '---':
                value[2] = 0
            if value[4].strip() == '---':
                value[4] = 0
            if value[5].strip() == '---':
                value[5] = 0
            if value[6].strip() == '---':
                value[6] = 0
            value[0] = value[0].strip(),
            value[8] = value[8].strip().replace(',', ''),
            value[9] = value[9].strip().replace(',', ''),
            value[10] = value[10].strip().replace(',', ''),
            value[11] = value[11].strip(),
            value[12] = value[12].strip(),
            value[13] = value[13].strip().replace(',', ''),
            value[15] = value[15].strip(),
            value[16] = value[16].strip()
            datalist.append((trade_date,
                            value[0], value[2], value[4], value[5], value[6],
                            value[8], value[9], value[10], value[11], value[12],
                            value[13], value[15], value[16]))
        return datalist

    # ==========================================================================
    # request by date
    # ==========================================================================
    def get_otc_dayily_close(self, dCrwaler):
        otc_d1 = datetime.datetime(2003, 8, 1)
        otc_d2 = datetime.datetime(2006, 12, 31)
        otc_d3 = datetime.datetime(2007, 1, 1)
        otc_d4 = datetime.datetime(2007, 4, 20)
        otc_d5 = datetime.datetime(2007, 4, 21)
        status = 0
        list_data = []

        if dCrwaler < otc_d1:
            logger.warning('Crawler day too long ago')
            status = 0

        if dCrwaler >= otc_d1 and dCrwaler <= otc_d2:
            logger.info('Crwaler before 2006-12-31')
            dom = self._get_before_951231(dCrwaler)
            json_data = self._get_before_951231_clean(dom)
            list_data = self._get_before_951231_filter(dCrwaler, json_data)
            status = 1

        if dCrwaler >= otc_d3 and dCrwaler <= otc_d4:
            # 96/01/02 ~ 96/04/20
            logger.info('Crwaler between 2007-01-01 and 2007-04-20')
            status = 1

        if dCrwaler >= otc_d5:
            logger.info('Crwaler after 2007-04-21')
            dom = self._get_after_960423(dCrwaler)
            json_data = json.loads(dom)
            list_data = self._get_after_960423_filter(json_data)
            status = 1

        return status, list_data
