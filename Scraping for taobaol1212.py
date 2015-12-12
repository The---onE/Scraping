#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
}

DATA = {
}

index = 1


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
    return string.decode('utf-8').encode('gbk')


def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html.content


def get_item(key, inf):
    if key in inf:
        return inf[key].encode('utf-8').replace(',', '.')
    else:
        return '-1'


def save_information(file, inf, sid, url):
    global index

    if len(inf) >= 14:
        num = get_item('item_num', inf)
        original_price = get_item('item_price', inf)
        title = get_item('item_title', inf)
        rule_id = get_item('sys_tce_scene_rule_id', inf)
        item_url = get_item('item_url', inf)
        current_price = get_item('item_dacu_price', inf)
        if current_price == '-1':
            current_price = get_item('item_current_price', inf)
        id = get_item('auction_id', inf)
        shop_url = get_item('item_shop_activity_url', inf)
        image_url = get_item('item_pic', inf)
        seller_id = get_item('seller_id', inf)
        app_id = get_item('app_id', inf)
        application_id = get_item('application_id', inf)
        shop_title = get_item('item_shop_title', inf)

        url = url.encode('utf-8')
        reg = r'1212/(.+?)/'
        infre = re.compile(reg)
        l = infre.findall(url)
        if len(l) > 0:
            url = l[0]
        else:
            reg = r'1212/(.+)'
            infre = re.compile(reg)
            l = infre.findall(url)
            url = l[0]

        codeinf = '%s' % index + '|' + id + '|' + title + '|' + current_price + '|' + original_price + '|' + item_url \
                  + '|' + shop_title + '|' + shop_url + '|' + image_url + '|' + num + '|' \
                  + url + '|' + rule_id + '|' + seller_id + '|' + app_id + '|' + application_id + '|' +sid
        print console_output(codeinf)

        fileinf = '%s' % index + ',' + id + ',' + title + ',' + current_price + ',' + original_price + ',' + item_url \
                  + ',' + shop_title + ',' + shop_url + ',' + image_url + ',' + num + ',' \
                  + url + ',' + rule_id + ',' + seller_id + ',' + app_id + ',' + application_id + ',' + sid + '\n'
        file.write(file_output(fileinf))

        index += 1


def get_information(file, html, url):
    reg = r'products[\s\S]*?tce_sid&quot;:(.+?)}'
    infre = re.compile(reg)
    tce_sid_list = infre.findall(html)

    for sid in tce_sid_list:
        print sid
        html = get_html('https://tce.taobao.com/api/mget.htm?tce_sid={0}'.format(sid))
        j = json.JSONDecoder().decode(html)
        inf_list = j['result'][sid]['result']

        for inf in inf_list:
            save_information(file, inf, sid, url)


if __name__ == '__main__':
    initial_page = 'https://tce.taobao.com/api/mget.htm?tce_sid=271376'
    initial_page = input_to_utf(initial_page)

    filename = raw_input('Input the file name of the csv you want to save to:')

    with open(input_to_gbk(filename) + '.csv', "w") as file:
        header = '序号,ID,商品,现价,原价,商品网址,店铺,店铺网址,图片网址,数量,分类,rule_id,seller_id,app_id,application_id,sid\n'
        file.write(file_output(header))
        h = get_html(initial_page)
        j = json.JSONDecoder().decode(h)
        l = j['result']['271376']['result']
        for i in l:
            url = i['url']
            html = get_html('https:' + url)
            get_information(file, html, url)
