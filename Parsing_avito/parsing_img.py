import requests
import os

def get_file(url):
    r = requests.get(url, stream=True)
    return r

def get_name(url, name_folder):
    name = url.split('/')[-1]

    if not os.path.exists('Parsing_avito/img/' + name_folder):
        os.makedirs('Parsing_avito/img/' + name_folder)

    return 'Parsing_avito/img/' + name_folder + '/' + name

def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)


def start_save_img(urls, name_folder):
    for url in urls:
        save_image(get_name(url, name_folder), get_file(url))
