import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.darty.com'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

productlinks = []

for x in range(1,2):
        r = requests.get(f'https://www.darty.com/nav/achat/informatique/ecran_informatique/page{x}.html')
        soup = BeautifulSoup(r.content, 'html.parser')

        productlist = soup.find_all('div', class_='product_detail next_prev_info')

        for item in productlist:
            for link in item.find_all('a', class_='next_prev', href=True):
                productlinks.append(baseurl + link['href'])


monitorlist = []
for link in productlinks:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        name = soup.find('span', class_='product_name font-2-b').text.strip()
        try:
            price = soup.find('div', class_='product-price__price').text.strip()
        except:
            price = 'no price no price no price'
        monitors = {
                'url' : link,
                'name' : name[0:50],
                'price' : price
                }

        monitorlist.append(monitors)


df = pd.DataFrame(monitorlist)
df.to_csv('drt-monitors.csv')
df.to_excel('drt-monitors.xlsx')
