# -*- coding: utf-8 -*-

import urllib.request
import json
import logging


logger = logging.getLogger('app')


def get_gimmeproxy_url(headers={}):
    url = 'http://gimmeproxy.com/api/getProxy?protocol=http'
    myRequest = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(myRequest)
    res = response.read().decode('utf-8')
    resJson = json.loads(res)
    return resJson['curl']


def update_urllib_proxy(proxy_url):
    ''' 更新urllib proxy '''
    proxy = proxy_url
    proxy_support = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    logger.info('urllilb proxy update to >>' + proxy_url)


def get_current_ip(headers={}):
    ''' 取得當前請求的IP '''
    check_url = 'http://icanhazip.com'
    myRequest = urllib.request.Request(check_url, headers=headers)
    response = urllib.request.urlopen(myRequest)
    res = response.read().decode('utf-8')
    logger.info('current proxy ip detect is : ' + res.strip())


def get_headers():
    ''' set headers '''
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    return headers
