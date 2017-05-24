# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import datetime


class OtcCrawler():
    def __init__(self, headers={}):
        self.headers = headers
        #
        self.url_1 = 'N/A'
        # 96/01/02  ~ 96/04/20
        self.url_2 = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotesB/stk_quote_result.php?'

    def get_every_stock_info(self, dCrwaler):
        dOtcStart = datetime.datetime(2007, 4, 23)
        if dCrwaler >= dOtcStart:
            response = self._get_every_after_960423(dCrwaler)
            res = response.read().decode('utf-8')
            resJson = json.loads(res)
            c_tradeDate = resJson['reportDate']
            print('日期: ' + c_tradeDate + ',   筆數: ' + str(resJson['iTotalRecords']))
            return resJson

    def _get_every_after_960423(self, dCrwaler):
        ''' after 96/04/23
            reportDate:    日期
            reportTitle:
            iTotalRecords: 資料總筆數
            iTotalDisplayRecords: 資料總顯示筆數
            listNum:     上櫃家數
            totalAmount: 總成交金額(元)
            totalVolumn: 總成交股數
            totalCount:  總交易筆數
            mmData: []
            aaData: [股票代號 ,股票名稱 ,收盤價 ,漲跌 ,開盤價 ,盤中最高 ,盤中最低 ,均價 ,成交股數,
                      成交金額(元) ,成交筆數 ,最後買價 ,最後賣價 ,發行股數 ,次日參考價 ,次日漲停價 ,次日跌停價]
        '''
        ttime = str(int(time.time()*100))
        date_str = '{0}/{1:02d}/{2:02d}'.format(dCrwaler.year - 1911, dCrwaler.month, dCrwaler.day)
        params = 'l=zh-tw&d={}&_={}'.format(date_str, ttime)
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?'
        request_url = url + params

        myRequest = urllib.request.Request(request_url, headers=self.headers)
        return urllib.request.urlopen(myRequest)


class TsecCrawler():
    '''
        tsec first day is 2004/02/11
    '''
    def test(self):
        print('tsec test.............')
