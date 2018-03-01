from lxml import html
import requests
import json

page = requests.get('https://www.ledc.com/tech-jobs')
tree = html.fromstring(page.content)

print(tree)

companys = tree.xpath('//*[@id="listing-tech-jobs"]/a/img/@alt')
urls = tree.xpath('//*[@id="listing-tech-jobs"]/a/@href')
results = dict(zip(companys, urls))
results_str = json.dumps(results)
loaded_r = json.loads(results_str)

with open('data.json', 'w') as outfile:
    json.dump(loaded_r, outfile)
