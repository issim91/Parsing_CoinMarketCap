# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from config import get_html, get_proxy, get_phone
from parsing_img import start_save_img, get_name


def get_items_description(url, sity_rus_name):
    # print('запустил get_item_description')
    sleep(uniform(15, 20))
    proxy, useragent = get_proxy()
    base_url = 'https://www.avito.ru/'
    all_url = base_url + url
    print('Парсинг товара - ' + all_url)
    try:
        html = get_html(all_url, proxy, useragent)
        soup = BeautifulSoup(html, "lxml")
        sleep(uniform(14, 18))
    except:
        print('Ошибка в получении HTML кода страницы' + all_url)

    # print('Начал парсить все о товаре')
    try:
        item_view = soup.find('div', class_='item-view')
        sleep(uniform(5, 7))
    except:
        print('Ошибка в карточке товара: ' + all_url)
    try:
        name = item_view.find('div', class_='item-view-header').find('span', class_='title-info-title-text').text.strip()
        sleep(uniform(5, 7))
    except:
        name = ''
    try:
        price = item_view.find('div', class_='item-view-header').find('span', class_='js-item-price').text.strip()
        sleep(uniform(3, 5))
    except:
        price = ''
    try:
        contact_name = item_view.find('div', class_='seller-info-name').find('a').text.strip()
        sleep(uniform(3, 5))
    except:
        contact_name = ''
    try:
        description = item_view.find('div', class_='item-description-text').find('p').text.strip()
        sleep(uniform(2, 6))
    except:
        description = ''
    
    # Парсинг картинок
    urls_img = []
    dir_img = []
    # Поиск главной картинки объявления
    try:
        main_img = item_view.find('div', class_='gallery-imgs-wrapper').find('img').get('src')
        urls_img.append('https:' + main_img)
        # Директория где сохраняется картинка
        dir = get_name(url, name, sity_rus_name)
        dir_img.append(dir)
    except:
        print('Нету главной картинки ' + all_url)
    # Поиск дополнительных картинок обявления
    try:
        sleep(uniform(2, 4))
        item_img = item_view.find('div', class_='gallery-list-wrapper').find_all('li')
        # счетчик картинок
        i_img = 0
        for item in item_img:
            # Первая картинка не парсится (главная картинка)
            if i_img == 0:
                i_img = i_img + 1
            # ограничение на парсинг картинок по заданному количетсву
            elif i_img < 3 and i_img > 0:
                i_img = i_img + 1
                url = item.find('span').get('style').split('//')[-1].split(')')[0].replace('75x55', '640x480')
                urls_img.append('https://' + url)
                # Директория где сохраняется картинка
                dir = get_name(url, name, sity_rus_name)
                dir_img.append(dir)
                sleep(uniform(1, 3))
            else:
                break
    except:
        print('Дополнительных картинок нет ' + all_url)
    # Сохранение картинок в папку с названием города и товара
    start_save_img(urls_img, name, sity_rus_name)
    # Парсинг номера телефона, через мибильную версию
    try:
        sleep(uniform(1, 3))
        mobile_url = all_url.replace('www', 'm')
        phone = get_phone(mobile_url)
    except:
        phone = ''

    return name, price, description, contact_name, phone, dir_img