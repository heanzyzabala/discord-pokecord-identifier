import json
import requests
import shutil
import cv2
import glob
import tempfile
import time
import os
import re
from bs4 import BeautifulSoup


def load():
    with open('resources/metadata.json') as json_file:
        metadata = json.load(json_file)
        context = []
        for file in glob.glob('resources/images/*.png'):
            context.append({
                'name': metadata[os.path.basename(file)],
                'image': cv2.imread(file)
            })
        return context


def save(url):
    res = requests.get(url, stream=True)
    with open('resources/temp.png', 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    return cv2.imread(f.name)


def find(supplied, context):
    for c in context:
        if compare(c['image'], supplied):
            return c['name']
    return None


def compare(src, supplied):
    if src.shape == supplied.shape:
        diff = cv2.subtract(src, supplied)
        b, g, r = cv2.split(diff)
        return cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0
    return False


def extract():
    t0 = time.time()
    print('Sending request..')
    res = requests.get('https://www.serebii.net/pokemon/all.shtml')
    print('Received response..')
    soup = BeautifulSoup(res.text, 'html.parser')

    paths = soup.findAll('a', href=re.compile("^(/pokemon/.[^/]+)$"), text=re.compile('.*'))

    print('Downloading images..')
    i = 0
    meta = {}
    for path in paths:
        parent = path.parent
        if parent.name == 'td':
            i += 1
            n = '{0:0>3}'.format(i)
            url = f'https://www.serebii.net/pokemon/art/{n}.png'
            print(f'Downloading from: {url}')
            res = requests.get(url, stream=True)
            if res.status_code == 200:
                with open(f'resources/images/{n}.png', 'wb') as f:
                    res.raw.decode_content = True
                    shutil.copyfileobj(res.raw, f)
                    meta[f'{n}.png'] = path.text
            else:
                print(f'*****Unable to download from: {url} - {res.status_code}')
    with open('resources/metadata.json', 'w') as m:
        json.dump(meta, m, indent=4)

    print('Done')
    t1 = '{:2f}'.format((time.time() - t0) / 60)
    print(f'Time elapsed: {t1} minutes')

