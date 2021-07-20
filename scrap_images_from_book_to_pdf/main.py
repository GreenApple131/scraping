import requests, time, img2pdf
from bs4 import BeautifulSoup


def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }

    img_list = []
    for x in range(1, 49):
        url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{x}.jpg"
        req_img = requests.get(url=url, headers=headers).content

        with open(f'media/{x}.jpg', 'wb') as image:
            image.write(req_img)
            img_list.append(f'media/{x}.jpg')

        print(f'Downloaded #{x} image..')

        # time.sleep(1)
    
    create_pdf(img_list)

def create_pdf(img_list):
# def create_pdf():
    # img_list = []
    # for x in range(1, 49):
    #     img_list.append(f'media/{x}.jpg')

    with open('result.pdf', 'wb') as f:
        f.write(img2pdf.convert(img_list))

    print('The work is done!')


def main():
    get_data()


if __name__ == '__main__':
    main()