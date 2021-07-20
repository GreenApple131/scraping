import requests, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }

    options = Options()
    options.add_argument('user-agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')

    try:
        driver = webdriver.Chrome(
            chrome_options=options,
            executable_path='/home/dmytro/Projects//python/devs_outstaff/tasks/scripts/parsing/parse_with_selenium/chromedriver'
        )
        driver.get(url=url)
        time.sleep(5)

        with open('index_selenium.html', 'w') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def parse_hotels():
    with open('index_selenium.html') as file:
        src = file.read()

    # get hotels url
    soup = BeautifulSoup(src, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')

    for hotel in hotels_cards:
        hotel_url = 'https://tury.ru/' + hotel.find('a').get('href')
        print(hotel_url)



def main():
    # get_data('https://tury.ru/hotel/most_luxe.php')
    parse_hotels()


if __name__ == '__main__':
    main() # get hotels urls with selenium