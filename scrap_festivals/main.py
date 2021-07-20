import requests, json, csv, random, time
from bs4 import BeautifulSoup


headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

fest_urls_list = []
for o in range(0, 193, 24):
    
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=13%20Jul%202021&to_date=&maxprice=500&o={o}&bannertitle=July"
    

    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f"data/index_{o}.html", "w", encoding='utf-8') as file:
        file.write(html_response)
    
    with open(f"data/index_{o}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    card_link = soup.find_all('a', class_='card-details-link')

    for l in card_link:
        fest_urls_list.append('https://www.skiddle.com' + l.get('href'))
    
    time.sleep(random.randint(2,5))

count = 0
fest_list_result = []
for url in fest_urls_list:
    count += 1
    print(count)
    req = requests.get(str(url), headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_info_block = soup.find("div", class_='top-info-cont')
        
        fest_name = fest_info_block.find('h1').text.strip()
        fest_date = fest_info_block.find('h3').text.strip()
        fest_location_url = 'https://www.skiddle.com' + fest_info_block.find('a', class_='tc-white').get('href')

        req = requests.get(url=fest_location_url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        contact_details = soup.find('h2', string='Venue contact details and info').find_next()
        items = [item.text for item in contact_details.find_all('p')]
    
        contact_details_dict={}
        
        for i in items:
            contact_details_list = i.split(':', 1)
            contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip()
        
        fest_list_result.append(
            {
                'Fest name': fest_name,
                'Fest date': fest_date,
                'Contacts data': contact_details_dict
            }
        )

    except Exception as ex:
        print(ex)
        print('Some error..')

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)

print("Scraping has been done!")
