# -*- coding: utf-8 -*-

import urllib2
import re

index = 1
world_area = 0

def input_to_utf(string):
    return string
    # return string.decode('gbk').encode('utf-8')


def input_to_gbk(string):
    # return string
    return string.decode('utf-8').encode('gbk')


def console_output(string):
    # return string.decode('utf-8').encode('gbk')
    return string


def file_output(string):
    return string.decode('utf-8').encode('gbk')


def get_html(url, data, headers):
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    # response = urllib2.urlopen(request, timeout=1)
    return response.read()


def save_information(file, inf, index):
    wiki = inf.group(1)
    name = inf.group(2)
    area = inf.group(3).replace(',', '')
    global world_area
    world_area += float(area)

    code_inf = '%s' % index + '|' + wiki + '|' + area
    print console_output(code_inf)

    if index == 188:
        return
    file_inf = '{ "name": "' + wiki + '", "value": ' + area + ' },\n'
    file.write(file_output(file_inf))

    if wiki != name:
        if index == 67 or index == 188:
            return
        file_inf = '{ "name": "' + name + '", "value": ' + area + ' },\n'
        file.write(file_output(file_inf))


def get_information(file, html):
    reg = r'data-wiki="(.*?)"[\s\S]*?sym\([\s\S]*?\)">(.*?)</a>[\s\S]*?"n">(.*?)</td>'
    inf_re = re.compile(reg)
    inf_list = inf_re.finditer(html)
    flag = False
    global index
    for inf in inf_list:
        flag = True
        save_information(file, inf, index)
        index += 1
    print index
    return flag


value = {}
data = None

headers = {}

filename = raw_input('Input the file name of the json you want to save to:')
url = 'http://world.bymap.org/LandArea.html'  # raw_input('Input the url you want to scrape:')
url = input_to_utf(url)

with open(input_to_gbk(filename) + '.json', "w") as file:
    head = '[\n'
    tail = ']'
    file.write(file_output(head))
    html = get_html(url, data, headers)
    get_information(file, html)
    world = '{ "name": "World", "value": ' + str(world_area) + ' }\n'
    file.write(file_output(world))
    file.write(file_output(tail))
