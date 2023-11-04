main_words = ['django', 'flask']

import requests
import bs4
import fake_headers
import json


headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=headers_gen.generate())
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')


main_vacancy_list_tag = main_soup.find('main', class_ = 'vacancy-serp-content')
vacancies_tags = main_vacancy_list_tag.find_all('div', class_ = 'serp-item')

parsed_data = []

for vacancy_tag in vacancies_tags:
    h3_tag = vacancy_tag.find('h3', class_ = 'bloko-header-section-3')
    a_tag = h3_tag.find('a')
    link_absolute = a_tag['href']
    header = h3_tag.text

    span_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}, class_ = 'bloko-header-section-2')
    if span_tag in vacancy_tag:
        salary = span_tag.text
    else:
        salary = 'не указана'

    div_tag = vacancy_tag.find('div', class_ = 'vacancy-serp-item__meta-info-company')
    employer = div_tag.text

    div2_tag = vacancy_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = div2_tag.text

    
    headers_gen2 = fake_headers.Headers(browser='chrome', os='win')
    response_link = requests.get(link_absolute, headers=headers_gen2.generate())

    link_html = response_link.text
    link_soup = bs4.BeautifulSoup(link_html, 'lxml')

    description_tag = link_soup.find('div', class_ = 'vacancy-description')
    description = description_tag.text.lower()
    if any([description in descr for descr in main_words]):
        parsed_data.append({
        'link': link_absolute,
        'header': header,
        'salary': salary,
        'employer': employer,
        'city': city
        })

if __name__ == '__main__':
    print(json.dumps(parsed_data, ensure_ascii=False))