from lxml import html
import requests
import json
from urllib.parse import urlparse


def getHTML(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    result = {}
    result['company'] = tree.xpath('//*[@id="listing-tech-jobs"]/a/img/@alt')
    result['url'] = tree.xpath('//*[@id="listing-tech-jobs"]/a/@href')
    return result


def getDomainFromUrl(url):
    o = urlparse(url)
    return o.netloc.replace('www.', '')


def writeIntoFile(data, file):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)


def main():
    result = getHTML('https://www.ledc.com/tech-jobs')
    resultList = []
    for index, company in enumerate(result['company']):
        item = {}
        item['url'] = result['url'][index]
        item['domain'] = getDomainFromUrl(item['url'])
        item['company'] = company
        resultList.append(dict(item))
    writeIntoFile(resultList, 'data.json')

if __name__ == '__main__':
    main()
