from bs4 import BeautifulSoup
import requests

# print('Sending request..')
# res = requests.get('https://www.serebii.net/pokemon/all.shtml')
# print('Received response..')
f = open('sample.txt')
soup = BeautifulSoup(f.read(), 'html.parser')
table = soup.select('table.dextable')[0]
rows = table.select('tr')
for row in rows:
    data = row.select('td.fooinfo > a')
    for d in data:
        print(data[0])
