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
vacancies_tags = main_vacancy_list_tag.find_all('div', class_ = 'vacancy-serp-item__layout')

parsed_data = []

for vacancy_tag in vacancies_tags:
    header_tag = vacancy_tag.find('a', class_='serp-item__title')
    header = header_tag.text
    link_absolute = header_tag['href']

    salary_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}, class_ = 'bloko-header-section-2')
    if not salary_tag:
        salary = 'не указана'
    else:
        salary = salary_tag.text

    employer_tag = vacancy_tag.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
    employer = employer_tag.text

    city_tag = vacancy_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text

    
    headers_gen2 = fake_headers.Headers(browser='chrome', os='win')
    response_link = requests.get(link_absolute, headers=headers_gen2.generate())

    link_html = response_link.text
    link_soup = bs4.BeautifulSoup(link_html, 'lxml')

    description_tag = link_soup.find('div', class_ = 'vacancy-description')
    description = description_tag.text.lower()
    for word in main_words:
        if word in description:
            parsed_data.append({
            'link': link_absolute,
            # 'header': header,
            'salary': salary,
            'employer': employer,
            'city': city
            })

# if __name__ == '__main__':
#     print(json.dumps(parsed_data, ensure_ascii=False))

if __name__ == '__main__':
    with open ('parsed-data.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, ensure_ascii=False)