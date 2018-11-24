# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pync             # уведомления MacOS
from time import sleep


# Получение HTML кода
def get_html():
    url = 'https://coinmarketcap.com'
    r = requests.get(url)
    return r.text

# Парсинг
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    btn = soup.find('tr', id='id-bitcoin').find('a', class_='price').text.strip()
    eth = soup.find('tr', id='id-ethereum').find('a', class_='price').text.strip()

    data = {
            'bitcoin': btn,
            'ethereum': eth
            }

    # Вывод уведомления для Mac OS
    pync.notify(data['bitcoin'], title='Bitcoin')
    sleep(3)
    # Вывод уведомления для Mac OS
    pync.notify(data['ethereum'], title='Ethereum')


def main():
    get_page_data(get_html())

if __name__ == '__main__':
    main()