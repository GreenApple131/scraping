import requests, json, csv, random
from bs4 import BeautifulSoup
from time import sleep


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',

}

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html') as file:
#     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_href] = item_text

# with open('all_categories_dict.json', 'w', encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)


count = 0
iteration_count = int(len(all_categories)) - 1
print(f"Iterations: {iteration_count}")

for category_href, category_name in all_categories.items():

    rep = [",", " ", "-", "'"]

    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # check if table exists
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue


    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    products_json = []
    for x in products_data:
        product_tds = x.find_all('td')
        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        products_json.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins":proteins,
                "Fats": fats,
                "Carbohudrates": carbohydrates
            }
        )
        with open(f"data/{count}_{category_name}", 'a', encoding="utf-8") as file:
            json.dump(products_json, file, indent=4, ensure_ascii=False)

        with open(f"data/{count}_{category_name}.csv", 'a', encoding='utf-8') as file:  # a - append, w - write(перезаписує)
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    count+=1
    print(f"# Iteration {count} - {category_name} writed..")
    iteration_count -= 1

    if iteration_count == 0:
        print('The work is done!')
        break
    
    print(f"Iterations left: {iteration_count}")
    sleep(random.randrange(2,4))