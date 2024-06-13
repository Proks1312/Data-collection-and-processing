import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)

db = client['vacancy_data_HH']
vacancy_mongo = db.vacancy_HH

search = input('Введите вакансию:')
if not search:
    search = 'python'

url = 'https://hh.ru/search/vacancy'
params = {'text': search, 'page': '0',
          'salary': ''}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
vacancies = []
pages_num = 0
while vacancies_list:
    for vacancy in vacancies_list:
        vacancy_data = {}
        info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        name = info.getText()
        link = info.get('href')
        try:
            salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).getText().replace('\u202f',
                                                                                                               '').replace(
                '\xa0', '-').split()
        except:
            salary = None
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        elif salary[0] == 'от':
            salary_min = salary[1]
            salary_max = None
            salary_currency = salary[2]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = salary[1]
            salary_currency = salary[2]
        else:
            salary_min = salary[0]
            salary_max = salary[2]
            salary_currency = salary[3]

    service_link = 'https://hh.ru'
    vacancy_data['name'] = name
    vacancy_data['link'] = link
    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['salary_currency'] = salary_currency
    vacancy_data['service_link'] = service_link
    vacancies.append(vacancy_data)
    pages_num += 1
    params['page'] = str(pages_num)
    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies_list = dom.find_all('div',
                                  {'class': 'vacancy-serp-item'})
    try:
        vacancy_mongo.insert_one({'_id': link,     #Задание №1
                                  'name': name,
                                  'link': link,
                                  'min_salary': salary_min,
                                  'max_salary': salary_max,
                                  'currency': salary_currency,
                                  'site_name': 'hh.ru'})
    except errors.DuplicateKeyError:
        continue

salary = 450000                                    #Задание №2

for a in vacancy_mongo.find({'$or': [{'salary_min': {'$gt': salary}},
                                     {'salary_max': {'$gt': salary}}]}):
    pprint(a)
