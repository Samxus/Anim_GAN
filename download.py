import os
import requests
import re


def find_max():
    dir_list = os.listdir('data/images')
    if len(dir_list) == 0:
        return 0
    files_index = []
    for file in dir_list:
        files_index.append(int(file.split('.')[0]))
    return max(files_index)


def download(url, user_agent='wswp', num_retries=2, proxy=None):
    print("Downloading...", url)
    headers = {'User_Agent': user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxy)
        html = resp.text
        if resp.status_code >= 400:
            print('Downloading error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Downloading error', e.reason)
    return html




url_root = 'https://safebooru.donmai.us/posts?page='
start = 1
if (len(os.listdir('data/images')) >= 0):
    start = int(len(os.listdir('data/images')) / 20) + 1
else:
    start = 1
if len(os.listdir('data/images')) >= 10000:
    print('Successfully Loading... {} images'.format(len(os.listdir('data/images'))))
else:
    while (True):
        url = url_root + str(start)
        html = download(url)
        path_list = re.findall('<source media="\(max-width: 660px\)" srcset="(.*?)"', html, re.S)
        for each in path_list:
            try:
                pic = requests.get(each, timeout=10)
            except requests.exceptions.ConnectionError as e:
                print('Downloading Error....')
                continue
            dir = 'data/images/' + str(find_max() + 1) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            print('Downloading: {} to {}'.format(each, dir))
            fp.close()
        start += 1
        if (len(os.listdir('data/images')) >= 10000):
            break
