import urllib2
import re

index = 1


def gethtml(url, data, headers):
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    # response = urllib2.urlopen(request, timeout=1)
    return response.read()


def saveinformation(file, inf, index, page):
    title = inf.group(1).replace(',', '.')
    price = inf.group(2).replace(',', '.')
    order = inf.group(3).replace(',', '.')
    print('%s' % index + '|' + title + '|' + price + '|' + order + '|' + '%s' % page)
    file.write('%s' % index + ',' + title + ',' + price + ',' + order + ',' + '%s' % page + '\n')


def getinformation(file, html, page):
    reg = r'(?:class="info"|class="detail")[\s\S]*?title="(.+?)"[\s\S]*?price">US \$(.+?)</span>[\s\S]*?Orders *\((.+?)\)</em>'
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
# url = 'http://www.aliexpress.com/wholesale?site=glo&g=y&SearchText=jewelry&page=%s&initiative_id=SB_20151130090930&shipCountry=US&needQuery=n'
url = raw_input('Input the url you want to scrape, use "%s" replace the page of your search:')

with open(filename + '.csv', "w") as file:
    header = 'Index,title,price,order,page\n'
    file.write(header)
    for i in range(1, maxpage + 1):
        html = gethtml(url % i, data, headers)
        if (getinformation(file, html, i) == False):
            break
