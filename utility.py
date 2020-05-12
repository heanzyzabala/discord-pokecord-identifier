import json
import requests
import shutil
import cv2
import glob
import tempfile
import time
import os
import re
import numpy as np
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DB = os.getenv('MONGO_DB')

mongo = MongoClient(MONGO_URL)
db = mongo[MONGO_DB]

dirname = os.path.dirname(__file__)


def load():
    with open(os.path.join(dirname, 'resources/metadata.json')) as json_file:
        metadata = json.load(json_file)
        if not db.pkmns.find_one({'is_loaded': {'$exists': True}}):
            for file in glob.glob(os.path.join(dirname, 'resources/images/*.png')):
                name = metadata[os.path.basename(file)]
                encoded_img = cv2.imencode('.png', cv2.imread(file))[1].tostring()
                db.pkmns.insert_one({'name': name, 'encoded_img': encoded_img})
            db.pkmns.insert_one({'is_loaded': True})
            print('Loaded images to db')
        else:
            print('Skipped loading images')


def find(url):
    res = requests.get(url, stream=True).raw
    img = np.asarray(bytearray(res.read()), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    for k in r.keys('pkmn-*'):
        v = r.get(k)
        np_arr = np.fromstring(v, np.uint8)
        img2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if compare(img, img2):
            name = k.decode('utf8').split('pkmn-')[1]
            r.incr(f'seen-{name}')
            return name
    return None


def compare(img0, img1):
    if img0.shape == img1.shape:
        diff = cv2.subtract(img0, img1)
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

