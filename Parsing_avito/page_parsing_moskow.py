# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from random import uniform
from time import sleep
from config import get_html, get_proxy, file_all_cat, delete_cat
from item_parsing import get_items_description
from multiprocessing import Pool
from datetime import datetime
import sys


def write_csv(data):
    with open('Parsing_avito/all_prod.csv', 'a', encoding="utf-8") as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['cat_name'],
                          data['sity_rus_name'],
                          data['name'],
                          data['price'],
                          data['description'],
                          data['contact_name'],
                          data['phone'],
                          data['dir_img']) )


# Поиск всех товаров на странице
def get_all_items(html, cat_name, sity_rus_name):
    # print('зашел в get_all_items')
    try:
        soup = BeautifulSoup(html, "lxml")
        # print(html)
        # print('создал суп')
        title_name = soup.find('title').text.strip()
        if title_name == 'Доступ временно заблокирован':
            sys.exit("------------------------------- Доступ временно заблокирован -------------------------------") 
        else:
            ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
            # print('нашел ads')
            sleep(uniform(3, 5))
            try:
                i = 0
                for ad in ads:
                    # print('for ads')
                    if i < 5:
                        start = datetime.now()
                        i = i + 1
                        # print('Прасинг ссылки на товар')
                        title_url = ad.find('div', class_='description').find('h3').find('a').get('href')
                        sleep(uniform(15, 18))
                        # print('Запуск поиска описания объявлений')
                        name, price, description, contact_name, phone, dir_img = get_items_description(title_url, sity_rus_name)

                        data_ads = {'cat_name': cat_name,
                                    'sity_rus_name': sity_rus_name,
                                    'name': name,
                                    'price': price,
                                    'description': description,
                                    'contact_name': contact_name,
                                    'phone': phone,
                                    'dir_img': dir_img}
                        # сохранение в файл всех данных о товаре
                        write_csv(data_ads)
                        end = datetime.now()
                        total = end - start
                        print('Добавил ' + data_ads['name'] + ' в csv файл.\n' + 'Время на парсинг товара : ' + str(total))
                    else:
                        break
            except:
                print('Ошибка в парсинге ссылки на карточку товара')
    except:
        print('Нету объявлений в городе ' + sity_rus_name + ' в категории - ' + cat_name)


def start_parsing(cat_url, cat_name):
    sleep(uniform(15, 20))
    proxy, useragent = get_proxy()
    sity_name = 'Москва'

    base_url = 'https://www.avito.ru/'
    sity_url = 'moskva'
    all_url = base_url + sity_url + cat_url
    try:
        # получаем страницу категории со всеми товарами
        html = get_html(all_url, proxy, useragent)
        sleep(uniform(15, 20))
        get_all_items(html, cat_name, sity_name)
        delete_cat(cat_name, cat_url)
        print('Категорию ' + cat_name + ' успешно спарсил')
    except:
        print('Ошибка парсинга! ' + proxy)

def main_parsing():
    start = datetime.now()
    cat_url, cat_name = file_all_cat()
    print('start multiprocessing parsing')
    with Pool(10) as p:
        p.starmap(start_parsing, zip(cat_url, cat_name))

    end = datetime.now()
    total = end - start
    print('Время на парсинг: ' + str(total))

if __name__ == '__main__':
    main_parsing()