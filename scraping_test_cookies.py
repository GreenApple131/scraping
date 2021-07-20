import requests, fake_useragent
from bs4 import BeautifulSoup

session = requests.Session()

link = ''
user = fake_useragent.UserAgent().randeom

header = {
    'user-agent': user
}

data = {
    'username': 'ga131',
    'password': '31231321'
}


login = session.post(link, headers=header, data=data).text


cookies_dict = {
    {'domain': key.domain, 'name': key.name, 'path': key.path, 'value': key.value}
    for key in session.cookies
}

session2 = requests.Session()

for cookies in cookies_dict:
    session2.cookies.set(**cookies)

resp = session2.get()
print(resp)