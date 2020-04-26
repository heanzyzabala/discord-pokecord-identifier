from bs4 import BeautifulSoup
import requests
import shutil
import re
import time
import json

t0 = time.time()
print('Sending request..')
res = requests.get('https://www.serebii.net/pokemon/all.shtml')
print('Received response..')
soup = BeautifulSoup(res.text, 'html.parser')

paths = soup.findAll('a', href=re.compile("^(/pokemon/.[^/]+)$"), text=re.compile('.*'))

print('Downloading images..')
i = 0
meta = []
for path in paths:
    parent = path.parent
    if parent.name == 'td':
        i += 1
        n = '{0:0>3}'.format(i)
        url = f'https://www.serebii.net/pokemon/art/{n}.png'
        # print(f'Downloading from: {url}')
        # res = requests.get(url, stream=True)
        # if res.status_code == 200:
        #     with open(f'resources/images/{n}.png', 'wb') as f:
        #         res.raw.decode_content = True
        #         shutil.copyfileobj(res.raw, f)
        meta.append({'id': n, 'name': path.text})
        # else:
        #     print(f'*****Unable to download from: {url} - {res.status_code}')
with open('resources/metadata.json', 'w') as m:
    json.dump(meta, m, indent=4)

print('Done')
t1 = '{:2f}'.format((time.time() - t0) / 60)
print(f'Time elapsed: {t1} minutes')
