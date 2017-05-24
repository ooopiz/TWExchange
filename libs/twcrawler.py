
import urllib.request
import time
import json


class OtcCrawler():
    def __init__(self, headers={}):
        self.headers = headers
        # after 96/04/23
        self.url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?'

    def get_otc_data(self, date_str):
        ttime = str(int(time.time()*100))
        params = 'l=zh-tw&d={}&_={}'.format(date_str, ttime)
        request_url = self.url + params

        myRequest = urllib.request.Request(request_url, headers=self.headers)
        response = urllib.request.urlopen(myRequest)
        res = response.read().decode('utf-8')
        resJson = json.loads(res)
        c_tradeDate = resJson['reportDate']
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

        print('日期: ' + c_tradeDate + ',   筆數: ' + str(resJson['iTotalRecords']))
        return resJson


class TseCrawler():
    '''
    tse first day is 2004/02/11
    '''
    def test(self):
        print('tse test.............')
