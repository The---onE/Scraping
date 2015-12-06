# -*- coding: utf-8 -*-

import urllib2
import re

index = 1


def inputtoutf(string):
    # return string
    return string.decode('gbk').encode('utf-8')


def inputtogbk(string):
    return string
    # return string.decode('utf-8').encode('gbk')


def consoleoutput(string):
    return string.decode('utf-8').encode('gbk')
    # return string


def fileoutput(string):
    return string.decode('utf-8').encode('gbk')


def gethtml(url, data, headers):
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    # response = urllib2.urlopen(request, timeout=1)
    return response.read()


def saveinformation(file, inf, index, page):
    id = inf.group(1).replace(',', '.')
    category = inf.group(2).replace(',', '.')
    title = inf.group(3).replace(',', '.')
    picture = inf.group(4).replace(',', '.')
    price = inf.group(5).replace(',', '.')
    location = inf.group(6).replace(',', '.')
    order = inf.group(7).replace(',', '.')
    if inf.group(8) == None:
        comment = '0'
    else:
        comment = inf.group(8).replace(',', '.')
    shop = inf.group(9).replace(',', '.')

    codeinf = '%s' % index + '|' + id + '|' + category + '|' + title + '|' + picture + '|' + price + '|' + location + '|' + order + '|' + comment + '|' + shop + '|' + '%s' % page
    print consoleoutput(codeinf)

    fileinf = '%s' % index + ',' + id + ',' + category + ',' + title + ',' + picture + ',' + price + ',' + location + ',' + order + ',' + comment + ',' + shop + ',' + '%s' % page + '\n'
    file.write(fileoutput(fileinf))


def getinformation(file, html, page):
    reg = r'"nid":"(.*?)","category":"(.*?)"[\s\S]*?raw_title":"([\s\S]*?)","pic_url":"//(.+?)"[\s\S]*?view_price":"(.*?)"[\s\S]*?item_loc":"(.*?)"[\s\S]*?sales":"(.*?)人付款"(?:,"comment_count":"([0-9]+?)")*[\s\S]+?nick":"(.*?)"'
    infre = re.compile(reg)
    inflist = infre.finditer(html)
    flag = False
    global index
    for inf in inflist:
        flag = True
        saveinformation(file, inf, index, page)
        index += 1
    return flag


value = {}
data = None

headers = {}

maxpage = input('Input the max page you want:')
filename = raw_input('Input the file name of the csv you want to save to:')
url = raw_input('Input the url you want to scrape, use "{0}" replace the page of your search:')
url = inputtoutf(url)

with open(inputtogbk(filename) + '.csv', "w") as file:
    fileinf = '序号,ID,分类,标题,图片,价格,地点,购买数,评论数,店铺,页面\n'
    file.write(fileoutput(fileinf))
    for i in range(1, maxpage + 1):
        html = gethtml(url.format((i - 1) * 44), data, headers)
        if not getinformation(file, html, i):
            break
