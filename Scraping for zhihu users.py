#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import os
import json
import re
import Queue
import codecs

INDEX = 1
MAX_USER = 1
URL_QUEUE = Queue.Queue()
SEEN_SET = set()

HOMEPAGE_URL = 'http://www.zhihu.com'
LOGIN_URL = 'http://www.zhihu.com/login/email'

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

DATA = {
    'email': '834489218@qq.com',
    'password': '1995n11y9r',
    'rememberme': "true",
}


def input_to_utf(string):
    # return string
    return string.decode('gbk').encode('utf-8')


def input_to_gbk(string):
    return string
    # return string.decode('utf-8').encode('gbk')


def console_output(string):
    return string.decode('utf-8').encode('gbk')
    # return string


def file_output(string):
    return string


def login(session):
    # 如果成功登陆过,用保存的cookies登录
    if os.path.exists('cookiefile'):
        with open('cookiefile') as f:
            cookie = json.load(f)
        session.cookies.update(cookie)
    # 第一次需要手动输入验证码登录
    else:
        req = session.get(HOMEPAGE_URL, headers=HEADERS)
        print req

        soup = BeautifulSoup(req.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')

        DATA['_xsrf'] = xsrf

        time_stamp = int(time.time() * 1000)
        captcha_url = 'http://www.zhihu.com/captcha.gif?=' + str(time_stamp)

        with open('zhihucaptcha.gif', 'wb') as f:
            captcha_req = session.get(captcha_url)
            f.write(captcha_req.content)
        login_captcha = raw_input('Input captcha:\n').strip()
        DATA['captcha'] = login_captcha
        # print data
        login_req = session.post(LOGIN_URL, headers=HEADERS, data=DATA)
        # print loginREQ.url
        # print s.cookies.get_dict()
        if not login_req.json()['r']:
            # print loginREQ.json()
            with open('cookiefile', 'wb') as f:
                json.dump(session.cookies.get_dict(), f)
        else:
            print 'login failed, try again!'
            return False
    return True


def get_html(url):
    html = s.get(url, headers=HEADERS)
    html.encoding = 'gbk'
    return html.content


def save_information(file, inf):
    global SEEN_SET
    global URL_QUEUE
    global INDEX

    link_url = inf.group(1).replace(',', '.')
    followees_url = link_url + '/followees'
    if followees_url not in SEEN_SET:
        nickname = inf.group(2).replace(',', '.')
        introduction = inf.group(3).replace(',', '.')
        followers = inf.group(4).replace(',', '.')
        asks = inf.group(5).replace(',', '.')
        answers = inf.group(6).replace(',', '.')
        walzer = inf.group(7).replace(',', '.')

        # code_inf = '%s' % INDEX + '|' + link_url + '|' + nickname + '|' + introduction + '|' \
        #           + followers + '|' + asks + '|' + answers + '|' + walzer
        code_inf = '%s' % INDEX + '|' + link_url + '|' + nickname + '|' \
                   + followers + '|' + asks + '|' + answers + '|' + walzer
        print console_output(code_inf)

        file_inf = '%s' % INDEX + ',' + link_url + ',' + nickname + ',' + introduction + ',' \
                   + followers + ',' + asks + ',' + answers + ',' + walzer + '\n'
        file.write(file_output(file_inf))

        SEEN_SET.add(followees_url)
        URL_QUEUE.put(followees_url)
        INDEX += 1


def get_information(file, html):
    global INDEX
    global MAX_USER

    reg = r'<a data-tip[\s\S]*?href="(.+?)"[\s\S]*?title="(.+?)">\2<[\s\S]*?gray">(.*?)<[\s\S]*?>(.*?) 关注者<[\s\S]*?>(.*?) 提问<[\s\S]*?>(.*?) 回答<[\s\S]*?>(.*?) 赞同'
    infre = re.compile(reg)
    inflist = infre.finditer(html)
    for inf in inflist:
        save_information(file, inf)
    return INDEX <= MAX_USER


if __name__ == '__main__':

    s = requests.session()
    login(s)

    initial_page = raw_input('Input the url you want to scrape:')
    initial_page = input_to_utf(initial_page)
    MAX_USER = input('Input the max page you want:')
    file_name = raw_input('Input the file name of the csv you want to save to:')

    SEEN_SET.add(initial_page)
    URL_QUEUE.put(initial_page)

    file = codecs.open(input_to_gbk(file_name) + '.csv', 'w')
    file.write(codecs.BOM_UTF8)
    while True:
        if URL_QUEUE.qsize() > 0:
            current_url = URL_QUEUE.get()  # 拿出队例中第一个的url
            html = get_html(current_url)
            if not get_information(file, html):
                break
        else:
            print 'No more user to show'
            break
    file.close()
