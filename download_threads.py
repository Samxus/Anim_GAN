import os
import requests
import re
import threading
import time

lock = threading.Lock()


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


def find_max():
    dir_list = os.listdir('data/images')
    if len(dir_list) == 0:
        return 0
    files_index = []
    for file in dir_list:
        files_index.append(int(file.split('.')[0]))
    return max(files_index)


def Download(url_root, start):
    url = url_root + str(start)
    html = download(url)
    path_list = re.findall('<source media="\(max-width: 660px\)" srcset="(.*?)"', html, re.S)
    print(threading.current_thread().name)
    for each in path_list:
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError as e:
            print('Downloading Error....')
            continue
        lock.acquire()
        dir = 'data/images/' + str(find_max() + 1) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        print('Downloading: {} to {}'.format(each, dir))
        fp.close()
        lock.release()


max_threads = 6
start = 1
threads = []
url_root = 'https://safebooru.donmai.us/posts?page='
if (len(os.listdir('data/images')) >= 0):
    start = int(len(os.listdir('data/images')) / 20) + 1
else:
    start = 1
while threads or start <= 500:
    for thread in threads:
        if not thread.is_alive():
            threads.remove(thread)
    while len(threads) < max_threads and start < 500:
        # can start some more threads
        thread = threading.Thread(target=Download, args=(url_root, start))
        start += 1
        thread.setDaemon(True)  # set daemon so main thread can exit w/ ctrl-c
        thread.start()

        threads.append(thread)
    print(threads)
    for thread in threads:
        thread.join()

    time.sleep(1)
