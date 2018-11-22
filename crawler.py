# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

# Получение HTML кода
def get_html(url):
    r = requests.get(url)  # Response
    return r.text # возвращает HTML код страницы (url)

# Парсинг
def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')

    links = []

    for td in tds:
        a = td.find('a').get('href')                # string
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links

# Парсинг имени и цены
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        rank = soup.find('span', class_='label label-success').text.strip()
    except:
        rank = 'Not Rank'

    try:
        name = soup.find('h1', class_='details-panel-item--name').text.strip()
    except:
        name = 'Not Name'

    try:
        price = soup.find('span', id='quote_price').text.strip()
    except:
        price ='Not Price'

    try:
        percentage = soup.find('span', attrs={'data-format-percentage':True}).text.strip()
    except:
        percentage ='Not Percentage'

    try:
        cap = soup.find('span', attrs={'data-currency-market-cap':True}).text.strip()
    except:
        cap ='Not Cap'

    data = {'rank': rank.strip('rankR'),
            'name': name,
            'price': price.strip('USD'),
            'percentage': percentage,
            'cap': cap.strip('USD')}
    return data

# Запись в файл
def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['rank'],
                          data['name'],
                          data['price'],
                          data['percentage'],
                          data['cap']) )
        
        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

def main():
    start = datetime.now()
    with open('coinmarketcap.csv', 'a', encoding='cp1251', newline='') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( ("Место",
                          "Название монеты",
                          "Цена (USD)",
                          "Динамика цен",
                          "Капитализация (USD)") )

    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links( get_html(url) )

    # map (function, list_)
    with Pool(10) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))

if __name__ == '__main__':
    main()