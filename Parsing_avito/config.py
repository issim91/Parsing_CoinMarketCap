import requests
from random import choice, uniform
from bs4 import BeautifulSoup

def get_html(url, useragent=None, proxy=None):
    s = requests.Session()
    r_cookie = s.get(url, headers=useragent, proxies=proxy)
    cookie = r_cookie.cookies
    print(cookie)
    print('---------------------------')
    # cookies = dict(cookies_are='working')
    # r = requests.get(url, cookies=cookies)
    r = s.get(url, headers=useragent, proxies=proxy, cookies=cookie)
    print(r.cookies)
    # print(r.text)
    # 'Set-Cookie': 'sessid=27d75dcaac2e65605ade1ab914910f7a.1543591643
    # u=2b7k8fgj.omudut.fxqi8ns4ro;
    # v=1543591643
    # dfp_group=8
    # print(r.cookies)
    return r.text

def get_proxy():
    useragents = open('Parsing_avito/useragent.txt').read().split('\n')
    proxies = open('Parsing_avito/proxy-ip.txt').read().split('\n')
    proxy = {'http': 'http://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}
    return proxy, useragent

def get_phone(url):
    proxy, useragent = get_proxy()
    html = get_html(url, proxy, useragent)
    soup = BeautifulSoup(html, "lxml")
    phone = soup.find('div', class_='_1DzgK').find('a').get('href').split(':')[-1]
    return phone