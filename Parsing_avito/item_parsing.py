import requests
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from config import get_html, get_proxy, get_phone
from parsing_img import start_save_img


def get_items_description(url):
    proxy, useragent = get_proxy()
    base_url = 'https://www.avito.ru/'
    sity_url = 'tolyatti' # динамическое значение
    cat_url = url
    all_url = base_url + sity_url + cat_url
    try: 
        html = get_html(all_url, proxy, useragent)
        
        soup = BeautifulSoup(html, "lxml")
        try:
            item_view = soup.find('div', class_='item-view')
            name = item_view.find('div', class_='item-view-header').find('span', class_='title-info-title-text').text.strip()
            price = item_view.find('div', class_='item-view-header').find('span', class_='js-item-price').text.strip()
            
            try:
                description = item_view.find('div', class_='item-description-text').find('p').text.strip()
            except:
                description = ''
            
            # Парсинг картинок
            try:
                item_img = item_view.find('div', class_='gallery-list-wrapper').find_all('li')
                i_img = 0
                urls_img = []
                for item in item_img:
                    # ограничение на парсинг картинок по заданному количетсву
                    if i_img < 3:
                        i_img = i_img + 1
                        url = item.find('span').get('style').split('//')[-1].split(')')[0].replace('75x55', '640x480')
                        urls_img.append('https://' + url)
                        sleep(uniform(0, 2))
                    else:
                        break
            except:
                urls_img = []
            # Сохранение картинок в папку с названием товара
            start_save_img(urls_img, name)

            # Парсинг номера телефона, через мибильную версию
            try:
                mobile_url = all_url.replace('www', 'm')
                phone = get_phone(mobile_url)
            except:
                phone = ''

        except:
            print('Fail parsing item descriprion')
            name = ''
            price = ''
            description = ''
            urls_img = []
            phone = ''    

        return name, price, description, phone, urls_img
    except:
        print('Item parsing - Fail proxy: ' + proxy)