import os, re, requests, fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random

header = {'user-agent': user}
link = 'https://hard.rozetka.com.ua/ua/memory/c80081/producer=g-skill;sort=cheap;21249=10836/'

response = requests.get(link, headers=header).text
soup = BeautifulSoup(response, 'lxml')

amount = soup.find_all('span', class_='goods-tile__title')

mem = {}
title = []
price = []

for x in range(0, 5):
    title.append(soup.find_all('span', class_='goods-tile__title')[x].text.strip())
    fixed_price = soup.find_all('span', class_='goods-tile__price-value')[x].text.strip()
    fixed_price = fixed_price.replace(u'\xa0', u'')
    price.append(int(fixed_price))



mem = {title[x]: price[x] for x in range(len(title))}
print(mem)
