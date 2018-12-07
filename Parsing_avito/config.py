import requests
from random import choice, uniform
from bs4 import BeautifulSoup
import csv

def get_html(url, useragent=None, proxy=None):
    timeout = uniform(15, 30)
    r = requests.get(url, headers=useragent, proxies=proxy, timeout=timeout)
    return r.text

def get_proxy():
    useragents = open('Parsing_avito/useragent.txt').read().split('\n')
    useragent = {'User-Agent': choice(useragents)}

    proxies = open('Parsing_avito/proxy-ip.txt', 'r')
    ip = str(proxies.readline()).replace("\n", "")
    proxy = {'http': 'http://' + ip}
    lines = proxies.readlines()
    proxies.close()

    proxies = open('Parsing_avito/proxy-ip.txt', 'w')
    for line in lines:
      if line != ip:
        proxies.write(line)
    proxies.write('\n')
    proxies.write(ip)
    proxies.close()
    return proxy, useragent


def file_all_cat():
    urls = open('Parsing_avito/cat.csv').read().split('\n')
    list_url = []
    list_name = []
    for url in urls:
            list_url.append(url.split(';')[-1])
            list_name.append(url.split(';')[0])
    return list_url, list_name

def file_all_sity():
    urls = open('Parsing_avito/all_sity.csv').read().split('\n')
    eng = []
    rus = []
    for url in urls:
            eng.append(url.split(';')[-1])
            rus.append(url.split(';')[0])
    return eng, rus

def delete_sity(eng, rus):
    sity = rus + ';' + eng + '\n'
    all_sity = open('Parsing_avito/all_sity.csv', 'r')
    lines = all_sity.readlines()
    all_sity.close()

    all_sity = open('Parsing_avito/all_sity.csv', 'w')
    for line in lines:
      if line != sity:
        all_sity.write(line)
    all_sity.close()


def delete_cat(cat_name, cat_url):
    cat = cat_name + ';' + cat_url + '\n'
    all_cat = open('Parsing_avito/cat.csv', 'r')
    lines = all_cat.readlines()
    all_cat.close()

    all_cat = open('Parsing_avito/cat.csv', 'w')
    for line in lines:
      if line != cat:
        all_cat.write(line)
    all_cat.close()
    

def get_phone(url):
    proxy, useragent = get_proxy()
    html = get_html(url, proxy, useragent)
    soup = BeautifulSoup(html, "lxml")
    phone = soup.find('div', class_='_1DzgK').find('a').get('href').split(':')[-1]
    return phone

# Добавляем названия столбцов в файле
def add_name_row():
    with open('Parsing_avito/all_prod.csv', 'a', encoding='cp1251', newline='') as f:
        writen = csv.writer(f, delimiter= ';')
        writen.writerow( (  "Название категории",
                            "Название товара",
                            "Цена",
                            "Описание",
                            "Номер телефона",
                            "Картинки") )