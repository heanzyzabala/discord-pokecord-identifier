from bs4 import BeautifulSoup
import requests
import shutil
import re
import time

print('Sending request..')
res = requests.get('https://www.serebii.net/pokemon/all.shtml')
print('Received response..')
soup = BeautifulSoup(res.text, 'html.parser')

paths = soup.findAll('a', href=re.compile("^(/pokemon/.[^/]+)$"), text=re.compile('.*'))

print('Downloading images..')
t0 = time.time()
i = 0
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
            pass
        else:
            print(f'*****Unable to download from: {url} - {res.status_code}')
print('Done')
t1 = '{:2f}'.format((time.time() - t0) / 60)
print(f'Time elapsed: {t1} minutes')
