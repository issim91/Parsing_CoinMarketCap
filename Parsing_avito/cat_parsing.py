# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from page_parsing import start_parsing, main_parsing
from random import uniform
from time import sleep
from config import get_html, get_proxy, add_name_row
from datetime import datetime
from multiprocessing import Pool


def write_csv(data):
    with open('Parsing_avito/all_cat.csv', 'a', encoding="utf-8") as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['cat_name'],
                          data['cat_url']) )

def get_all_cat(html):
    soup = BeautifulSoup(html, "lxml")
    cat_list = soup.find('ul', class_='rubricator-submenu-18HMk').find_all('li', class_='rubricator-item-31NYs')

    for cat in cat_list:
        try:
            cat_url = cat.find('a').get('href').split('?')[-2].replace('/tolyatti/', '/')
            cat_name = cat.find('a').text.strip()
            print('Парсинг категории: ' + cat_name + ' начал')
            sleep(uniform(3, 4))
        except:
            cat_url = ''
            cat_name = ''
        data = {'cat_name': cat_name, 'cat_url': cat_url}
        write_csv(data)

    print('Все категории спарсил')        

def start_parsing_cat():
    try:
        url = 'https://www.avito.ru/tolyatti/transport'
        proxy, useragent = get_proxy()
        html = get_html(url, useragent, proxy)
        # print(html)
        sleep(uniform(5, 7))
        get_all_cat(html)
    except:
        print('Cat Parsing - Fail proxy: ' + str(proxy))


def main():
    start = datetime.now()
    
    url = [
            'https://www.avito.ru/tolyatti/transport',
            'https://www.avito.ru/tolyatti/nedvizhimost',
            'https://www.avito.ru/tolyatti/rabota',
            'https://www.avito.ru/tolyatti/predlozheniya_uslug',
            'https://www.avito.ru/tolyatti/lichnye_veschi',
            'https://www.avito.ru/tolyatti/dlya_doma_i_dachi',
            'https://www.avito.ru/tolyatti/bytovaya_elektronika',
            'https://www.avito.ru/tolyatti/hobbi_i_otdyh',
            'https://www.avito.ru/tolyatti/zhivotnye',
            'https://www.avito.ru/tolyatti/dlya_biznesa',
    ]

    with Pool(10) as p:
        p.map(start_parsing_cat, url)

    end = datetime.now()
    total = end - start
    print('--------------------------------------------------------------')
    print('Время на парсинг ' + str(total))

if __name__ == "__main__":
    main()