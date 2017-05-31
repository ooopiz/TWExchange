# -*- coding: utf-8 -*-

import urllib.request
import json
import logging
import os

logger = logging.getLogger('app')


this_path = os.path.abspath(os.path.dirname(__file__))
PROXY_FILE = os.path.join(this_path, "../config/proxy")
LOG_FILE = os.path.join(this_path, "../logs/app.log")


def get_headers():
    ''' set headers '''
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    return headers


def set_logger(log_file=''):
    ''' set logger '''
    if log_file == '':
        log_file = LOG_FILE
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(name)-3s - %(levelname)-8s] %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            handlers=[logging.FileHandler(log_file, 'a', 'utf-8')])

    formatter = logging.Formatter('%(asctime)s [%(levelname)-7s] : %(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    applogger = logging.getLogger('app')
    applogger.addHandler(console)
    applogger.setLevel(logging.DEBUG)


def get_gimmeproxy_url(headers={}):
    ''' get proxy ip '''
    url = 'http://gimmeproxy.com/api/getProxy?protocol=http'
    myRequest = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(myRequest)
    res = response.read().decode('utf-8')
    resJson = json.loads(res)
    return resJson['curl']


def update_urllib_proxy():
    ''' update urllib proxy ip '''
    proxy_url = get_proxyurl_from_file()
    proxy_support = urllib.request.ProxyHandler({'http': proxy_url})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    logger.info('urllilb proxy update to >>  ' + proxy_url)


def get_current_ip(headers={}):
    ''' 取得當前請求的IP '''
    check_url = 'http://icanhazip.com'
    myRequest = urllib.request.Request(check_url, headers=headers)
    response = urllib.request.urlopen(myRequest)
    res = response.read().decode('utf-8')
    logger.info('Current proxy ip detect is : ' + res.strip())


def get_proxyurl_from_file():
    proxy_file = PROXY_FILE
    if not os.path.isfile(proxy_file):
        update_proxy_file()
    r_file = open(proxy_file, 'r')
    proxy_url = r_file.read()
    proxy_url = proxy_url.strip()
    r_file.close()
    return proxy_url


def update_proxy_file():
    proxy_file = PROXY_FILE
    proxy_url = get_gimmeproxy_url(get_headers())
    w_file = open(proxy_file, 'w')
    w_file.write(proxy_url)
    w_file.close()
    logger.info('Updating proxy file ...')
