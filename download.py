from Crawler.request_pack.test1 import download
import os
import requests
import re

indx = 1

url_root = 'https://safebooru.donmai.us/posts?page='
start = 1
if len(os.listdir('data/images')) >= 1000:
    print('Successfully Loading... {} images'.format(len(os.listdir('data/images'))))
else:
    while (True):
        url = url_root + str(start)
        html = download(url)
        path_list = re.findall('<source media="\(max-width: 660px\)" srcset="(.*?)"', html, re.S)
        for each in path_list:
            try:
                pic = requests.get(each, timeout=1)
            except requests.exceptions.ConnectionError as e:
                print('Downloading Error....')
                continue
            dir = 'data/images/' + str(indx) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            print('Downloading: {} to {}'.format(each, dir))
            indx += 1
            fp.close()
        start += 1
        if (len(os.listdir('data/images')) >= 1000):
            break
