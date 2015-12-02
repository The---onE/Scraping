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
    title = inf.group(2).replace(',', '.')
    picture = inf.group(3).replace(',', '.')
    price = inf.group(4).replace(',', '.')
    order = inf.group(5).replace(',', '.')
    codeinf = '%s' % index + '|' + id + '|' + title + '|' + picture + '|' + price + '|' + order + '|' + '%s' % page
    print consoleoutput(codeinf)

    fileinf = '%s' % index + ',' + id + ',' + title + ',' + picture + ',' + price + ',' + order + ',' + '%s' % page + '\n'
    file.write(fileoutput(fileinf))


def getinformation(file, html, page):
    reg = r'"nid":"(.+?)",[\s\S]*?raw_title":"([\s\S]+?)","pic_url":"//(.+?)"[\s\S]*?view_price":"(.+?)"[\s\S]*?sales":"(.+?)人付款"'
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
    for i in range(1, maxpage + 1):
        html = gethtml(url.format((i - 1) * 44), data, headers)
        if not getinformation(file, html, i):
            break
