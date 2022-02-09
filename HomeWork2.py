import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

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

final_data = pd.DataFrame(vacancies)
final_data.to_csv('HomeWork2(hh)', encoding="utf-8-sig")
print(final_data)
