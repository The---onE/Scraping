#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import urllib
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


def save_information(file, inf, index):
    if len(inf) >= 14:
        num = inf['item_num'].encode('utf-8').replace(',', '.')
        preorder = inf['item_pre_current'].encode('utf-8').replace(',', '.')
        original_price = inf['item_price'].encode('utf-8').replace(',', '.')
        title = inf['item_title'].encode('utf-8').replace(',', '.')
        aim = inf['item_pre_text'].encode('utf-8').replace(',', '.')
        if 'sys_tce_scene_rule_id' in inf:
            rule_id = inf['sys_tce_scene_rule_id'].encode('utf-8').replace(',', '.')
        else:
            rule_id = '0'
        item_url = inf['item_url'].encode('utf-8').replace(',', '.')
        current_price = inf['item_current_price'].encode('utf-8').replace(',', '.')
        id = inf['auction_id'].encode('utf-8').replace(',', '.')
        shop_url = inf['item_shop_activity_url'].encode('utf-8').replace(',', '.')
        image_url = inf['item_pic'].encode('utf-8').replace(',', '.')
        seller_id = inf['seller_id'].encode('utf-8').replace(',', '.')
        app_id = inf['app_id'].encode('utf-8').replace(',', '.')
        application_id = inf['application_id'].encode('utf-8').replace(',', '.')
        shop_title = inf['item_shop_title'].encode('utf-8').replace(',', '.')

        codeinf = '%s' % index + '|' + id + '|' + title + '|' + current_price + '|' + original_price + '|' + item_url\
                  + '|' + preorder + '|' + shop_title + '|' + shop_url + '|' + image_url + '|' + aim + '|' + num + '|' \
                  + rule_id + '|' + seller_id + '|' + app_id + '|' + application_id
        print console_output(codeinf)

        fileinf = '%s' % index + ',' + id + ',' + title + ',' + current_price + ',' + original_price + ',' + item_url \
                  + ',' + preorder + ',' + shop_title + ',' + shop_url + ',' + image_url + ',' + aim + ',' + num + ',' \
                  + rule_id + ',' + seller_id + ',' + app_id + ',' + application_id + '\n'
        file.write(file_output(fileinf))


def get_information(file, html):
    global index

    reg = r'&quot;items[\s\S]*?tce_sid&quot;:([0-9]*)}'
    infre = re.compile(reg)
    tce_sid_list = infre.findall(html)

    for sid in tce_sid_list:
        print sid
        html = get_html('https://tce.taobao.com/api/mget.htm?tce_sid={0}'.format(sid))
        j = json.JSONDecoder().decode(html)
        inf_list = j['result'][sid]['result']

        for inf in inf_list:
            save_information(file, inf, index)
            index += 1


if __name__ == '__main__':
    initial_page = raw_input('Input the url you want to scrape:')
    initial_page = input_to_utf(initial_page)

    filename = raw_input('Input the file name of the csv you want to save to:')

    with open(input_to_gbk(filename) + '.csv', "w") as file:
        html = get_html(initial_page)
        get_information(file, html)
