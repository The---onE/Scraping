#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import HTMLParser
import codecs
import urllib

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
}

DATA = {
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
    return string.decode('utf-8').encode('gbk')


def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html.content


def save_information(file, inf, index):
    h = HTMLParser.HTMLParser()
    logo = h.unescape(inf.group(1)).replace(',', '.').encode('utf-8')
    coupon = inf.group(2).replace(',', '.')
    desc = inf.group(3).replace(',', '.')
    id = inf.group(4).replace(',', '.')
    image = h.unescape(inf.group(5)).replace(',', '.').encode('utf-8')
    title = inf.group(6).replace(',', '.')
    url = h.unescape(inf.group(7)).replace(',', '.').encode('utf-8')
    price_title = inf.group(8).replace(',', '.')
    price = inf.group(9).replace(',', '.')
    handsel = inf.group(10).replace(',', '.')

    urllib.urlretrieve('http://' + logo, 'logo%s.jpg' % index)
    urllib.urlretrieve('http://' + image, 'image%s.jpg' % index)

    codeinf = '%s' % index + '|' + id + '|' + title + '|' + desc + '|' + logo + '|' + image + '|' + price_title + '|' + price + '|' + handsel + '|' + coupon + '|' + url + '|'
    print console_output(codeinf)

    fileinf = '%s' % index + ',' + id + ',' + title + ',' + desc + ',' + logo + ',' + image + ',' + price_title + ',' + price + ',' + handsel + ',' + coupon + ',' + url + '\n'
    file.write(file_output(fileinf))


def get_information(file, html):
    reg = r'brandLogo&quot;:&quot;&#x2F;&#x2F;(.+?)&quot[\s\S]*?couponValue&quot;:&quot;([0-9]*?)&quot[\s\S]*?itemDesc&quot;:&quot;(.+?)&quot[\s\S]*?itemId&quot;:&quot;([0-9]*?)&quot[\s\S]*?itemImgPC&quot;:&quot;&#x2F;&#x2F;(.+?)&quot[\s\S]*?itemTitle&quot;:&quot;(.+?)&quot;,&quot;itemUrl&quot;:&quot;&#x2F;&#x2F;(.+?)&quot[\s\S]*?preSaleExpandPriceTitleM&quot;:&quot;(.*?)&quot[\s\S]*?preSalePrice&quot;:&quot;([0-9]*?)&quot[\s\S]*?prepSaleHandsel&quot;:&quot;([0-9]*?)&quot'
    infre = re.compile(reg)
    inflist = infre.finditer(html)
    x = 1
    print 'Start'
    for inf in inflist:
        save_information(file, inf, x)
        x += 1
    print 'End'


if __name__ == '__main__':
    initial_page = raw_input('Input the url you want to scrape:')
    initial_page = input_to_utf(initial_page)
    filename = raw_input('Input the file name of the csv you want to save to:')
    with open(input_to_gbk(filename) + '.csv', "w") as file:
        fileinf = '序号,ID,标题,介绍,Logo网址,图片网址,优惠,价格,定金,券,网址\n'
        file.write(file_output(fileinf))
        html = get_html(initial_page)
        get_information(file, html)
