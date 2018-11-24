import requests
import os

urls = {
    'https://www.hdwallpapers.in/thumbs/2018/3d_triangles_5k-t2.jpg',
    'https://www.hdwallpapers.in/thumbs/2018/san_francisco_bay_bridge-t2.jpg',
    'https://www.hdwallpapers.in/thumbs/2018/mso_mclaren_720s_stealth_theme_2018_4k-t2.jpg',
    'https://www.hdwallpapers.in/thumbs/2018/macaw_parrot_4k-t2.jpg',
    'https://www.hdwallpapers.in/thumbs/2018/surreal_dream_5k-t2.jpg',
    'https://www.hdwallpapers.in/thumbs/2018/cute_girl_and_rabbit-t2.jpg'
}


def get_file(url):
    r = requests.get(url, stream=True)
    return r

def get_name(url):
    name = url.split('/')[-1]

    if not os.path.exists('img'):
        os.makedirs('img')

    return 'img/' + name

def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)


def main():
    for url in urls:
        save_image(get_name(url), get_file(url))


if __name__ == '__main__':
    main()
