import requests
from bs4 import BeautifulSoup
import csv
from random import uniform
from time import sleep
from config import get_html, get_proxy
from item_parsing import get_items_description


def write_csv(data):
    with open('Parsing_avito/all_prod.csv', 'a') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (data['name'],
                          data['price'],
                          data['description'],
                          data['phone'],
                          data['urls_img']) )


def get_all_items(html):
    soup = BeautifulSoup(html, "lxml")
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')    
    i = 0
    for ad in ads:
        if i < 5:
            i = i + 1
            print('Прасинг ' + i + ' товара')
            try:
                print('start search')
                title_url = ad.find('div', class_='description').find('h3').find('a').get('href').replace('/tolyatti/', '/')
                sleep(uniform(1, 3))
                name, price, description, phone, urls_img = get_items_description(title_url)
            except:
                print('Fail')                

            data_ads = {'name': name,
                        'price': price,
                        'description': description,
                        'phone': phone,
                        'urls_img': urls_img}
            # сохранение в файл всех данных о товаре
            write_csv(data_ads)
        else:
            print("Ending parsing all product")
            break


def start_parsing(url):
    proxy, useragent = get_proxy()
    print('new proxy')
    base_url = 'https://www.avito.ru/'
    sity_url = 'tolyatti' # динамическое значение
    cat_url = url
    all_url = base_url + sity_url + cat_url

    # for i in range(0, 5):
    try:
        print('Попытка парсить')
        html = get_html(all_url, proxy, useragent)
        get_all_items(html)
        # break
    except:
        print('Page Parsing - Fail proxy: ' + proxy)

# if __name__ == "__main__":
#     start_parsing()