import requests, time, json
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*'
    }

    url = 'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=12&noFilterSet=true'

    r = requests.get(url=url)

    mc = BeautifulSoup(r.text, 'lxml')

    members_count = int(mc.find('div').get('data-hits'))

    data = []
    counter = 0
    for i in range(0, members_count, 20):
        u = f'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158?limit=20&noFilterSet=true&offset={i}'

        req = requests.get(url=u).content

        soup = BeautifulSoup(req, 'lxml')

        cards = soup.find_all('div', class_='bt-slide-content')

        for x in cards:
            social_networks = []

            person_name = x.find('div', class_='bt-bild-info-text').find('p').text.strip()
            party_name = x.find('p', class_='bt-person-fraktion').text.strip()
            
            # collect social networks data
            link_to_perosnal_page = x.find('a').get('href')
            req_personal_page = requests.get(url=link_to_perosnal_page, headers=headers)
            sl = BeautifulSoup(req_personal_page.content, 'lxml')
            # social_links = sl.find('ul', class_='bt-linkliste').find_all('li')
            social_links = sl.find('h5', string='Profile im Internet')
            if social_links is not None:
                    social = social_links.find_next('ul', class_='bt-linkliste').find_all('li')
                    for i in social:
                        social_networks.append(i.find('a').get('href'))
            else:
                social_networks.append('Empty.')
            
            data.append(
                {
                    'person_name': person_name,
                    'party_name': party_name,
                    'social_networks': social_networks
                }
            )
        counter += 20
        print(f'Processed #{counter}/{members_count} members..')
        time.sleep(1)

    with open('result.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print('Work is done!')


def main():
    get_data()


if __name__ == '__main__':
    main()