# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split("&")[0]
    
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['title'],
                          data['price'],
                          data['geo'],
                          data['date'],
                          data['url']) )
        
        print(data['title'], 'parsed')

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")

    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    for ad in ads:
        name = ad.find('div', class_='description').find('h3').text.strip().lower()

        if 'htc' in name:

            try:
                title = ad.find('div', class_='description').find('h3').text.strip()
            except:
                title = 'None Title'

            try:
                url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
            except:
                url = 'None Url'

            try:
                price = ad.find('div', class_='about').find('span', class_='price').text.strip()
            except:
                price = 'None Price'

            try:
                geo = ad.find('div', class_='data').find_all('p')[-1].text.strip()
            except:
                geo = 'None Geo'

            try:
                date = ad.find('div', class_='data').find('div', class_='js-item-date').text.strip()
            except:
                date = 'None Data'

            data = {'title': title,
                    'price': price,
                    'geo': geo,
                    'date': date,
                    'url': url}
            write_csv(data)
        else:
            continue
            

def main():
    url = 'https://www.avito.ru/tolyatti/telefony?p=1&q=hts'
    base_url = 'https://www.avito.ru/tolyatti/telefony?'
    page_part = 'p='
    query_part = '&q=hts'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages+1):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)



if __name__ == "__main__":
    main()