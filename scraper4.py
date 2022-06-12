import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.bol.com'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

productlinks = []

for x in range(1,31):
        r = requests.get(f'https://www.bol.com/nl/nl/l/monitoren/10460/?page={x}')
        soup = BeautifulSoup(r.content, 'html.parser')

        productlist = soup.find_all('li', class_='product-item--row')

        for item in productlist:
            for link in item.find_all('a', class_='product-title', href=True):
                productlinks.append(baseurl + link['href'])
        
    
monitorlist = []
for link in productlinks:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        name = soup.find('h1', class_='page-heading').text.strip()
        
        try:
            price = soup.find('div', class_='price-block__highlight').text.strip()    
        except:    
            price = 'no price no price no price'
        else:
            try:
                stock = soup.find('div', class_='buy-block--with-highlight').text.strip()
            except:    
                stock = 'no stock no stock no stock'
        monitors = {
                'url' : link,
                'name' : name[0:50],
                'price' : price,
                'stock' : stock[0:12]
                }
                
        monitorlist.append(monitors)
        
        
df = pd.DataFrame(monitorlist)
df.to_csv('bol-monitors.csv')
df.to_excel('bol-monitors.xlsx')
print('saved to file')

