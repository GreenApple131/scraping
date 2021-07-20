import requests, time, os, json, csv
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }

    # r = requests.get(url='https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply')

    # if not os.path.exists('data'):
    #     os.mkdir('data')

    # with open('data/page_1.html', 'w') as file:
    #     file.write(r.text)

    with open('data/page_1.html') as file:
        src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='bx-pagination-container').find_all('a')[-2].text)
    
    for i in range(1, pages_count + 1):
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}'

        r = requests.get(url=url, headers=headers)
        with open(f'data/page_{i}.html', 'w') as file:
            file.write(r.text)

        time.sleep(2)
    
    return pages_count + 1




def collect_data(pages_count=6):
    cur_date = datetime.now().strftime('%d_%m_%Y')
    data = []

    with open(f'data_{cur_date}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Articul',
                'URL',
                'Price'
            )
        )

    for page in range(1, pages_count):
        with open(f'data/page_{page}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        item_cards = soup.find_all('a', class_='product-item__link')

        for item in item_cards:
            product_articul = item.find('p', class_='product-item__articul').text.strip()
            product_price = item.find('p', class_='product-item__price').text.lstrip("руб. ")
            product_url = 'https://shop.casio.ru' + item.get('href')
            # print(f'Article: {product_articul} - price: {product_price} - url: {product_url}')

            data.append(
                {
                    'product_articul': product_articul,
                    'product_url': product_url,
                    'product_price': product_price,

                }
            )
        
            with open(f'data_{cur_date}.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product_articul,
                        product_url,
                        product_price
                    )
                )


        print(f'Processed {page}/{pages_count-1} pages')

    with open(f'data_{cur_date}.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    


def main():
    # pages_count = get_data()
    collect_data()

if __name__ == '__main__':
    main()