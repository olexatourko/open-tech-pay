from lxml import html
import requests
import json
from urllib.parse import urlparse


def getHTML(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    result = {}
    result['name'] = tree.xpath('//*[@id="listing-tech-jobs"]/a/img/@alt')
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
    for index, company in enumerate(result['name']):
        item = {}
        item['url'] = result['url'][index]
        item['email_domain'] = getDomainFromUrl(item['url'])
        item['name'] = company
        resultList.append(dict(item))
    print(json.dumps(resultList, indent=4))

if __name__ == '__main__':
    main()
