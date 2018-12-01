import requests
from bs4 import BeautifulSoup
import csv
from page_parsing import start_parsing
from random import uniform
from time import sleep
from config import get_html, get_proxy
from datetime import datetime


def write_csv(data):
    with open('Parsing_avito/all_cat.csv', 'a') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['cat_name'],
                          data['cat_url']) )

def get_all_cat(html):
    soup = BeautifulSoup(html, "lxml")
    cat_list = soup.find('ul', class_='rubricator-submenu-18HMk').find_all('li', class_='rubricator-item-31NYs')
    for cat in cat_list:
        start = datetime.now()
        try:
            cat_url = cat.find('a').get('href').split('?')[-2].replace('/tolyatti/', '/')
            cat_name = cat.find('a').text.strip()
            sleep(uniform(2, 5))
            # start_parsing(cat_url)
        except:
            cat_url = ''
            cat_name = ''

        print('Парсинг категории: ' + cat_name)
        print(cat_url)
        data = {'cat_name': cat_name, 'cat_url': cat_url}
        write_csv(data)
    
        end = datetime.now()
        total = end - start
        print('Время на парсинг категории ' + str(total))
    print('---------------------------------')
        
def main():
    proxy, useragent = get_proxy()

    url = [
            'https://www.avito.ru/tolyatti/transport',
            # 'https://www.avito.ru/tolyatti/nedvizhimost',
            # 'https://www.avito.ru/tolyatti/rabota',
            # 'https://www.avito.ru/tolyatti/predlozheniya_uslug',
            # 'https://www.avito.ru/tolyatti/lichnye_veschi',
            # 'https://www.avito.ru/tolyatti/dlya_doma_i_dachi',
            # 'https://www.avito.ru/tolyatti/bytovaya_elektronika',
            # 'https://www.avito.ru/tolyatti/hobbi_i_otdyh',
            # 'https://www.avito.ru/tolyatti/zhivotnye',
            # 'https://www.avito.ru/tolyatti/dlya_biznesa',
    ]

    for i in url:
        try:
            html = get_html(i, useragent, proxy)
            get_all_cat(html)
        except:
            print('Cat Parsing - Fail proxy: ' + str(proxy))


if __name__ == "__main__":
    main()