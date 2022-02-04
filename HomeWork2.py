import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

url = 'https://hh.ru/search/vacancy?clusters=true&area=1&area=232&area=113&ored_clusters=true&enable_snippets=true&salary='
params = {'text': input('Введите вакансию:'), 'page': input('Введите страницу для парсинга:'),
          'hhtmFrom': 'vacancy_search_list'}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

vacancies = []
for vacancy in vacancies_list:
    vacancy_data = {}
    info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    name = info.getText()
    link = info.get('href')
    company = vacancy.find('a', {'class': "bloko-link bloko-link_kind-secondary"}).getText()
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).
    service_link = 'https://hh.ru'
    vacancy_data['name'] = name
    vacancy_data['link'] = link
    vacancy_data['company'] = company
    vacancy_data['salary'] = salary
    vacancy_data['service_link'] = service_link
    vacancies.append(vacancy_data)
    final_data = pd.DataFrame(vacancies)
    final_data.to_csv('HomeWork2')
pprint(final_data)
