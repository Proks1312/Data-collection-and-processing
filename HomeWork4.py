from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests

url = 'https://lenta.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)

client = MongoClient('127.0.0.1', 27017)
db = client['news_data']
news_data = db.news_collection
news_data.drop()
news_data.create_index('link', name='link_index', unique=True)

dom = html.fromstring(response.text)
items = dom.xpath('//div/a[contains(@class,"card-") and contains(@class,"_topnews")]')

news_list = []
for item in items:
    name = item.xpath('.//*[contains(@class,"_title")]/text()')[0]
    link = url + item.get('href')
    time_publication = item.xpath(".//time[@class = 'card-mini__date']/text()")
    service = 'lenta.ru'
    news = {
        'name': name,
        'link': link,
        'time_publication': time_publication,
        'service': service
    }
    news_list.append(news)
    try:
        news_data.insret_one(news_list)
    except:
        pass

pprint(news_list)
