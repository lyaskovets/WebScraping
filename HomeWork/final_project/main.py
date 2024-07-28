import requests
from bs4 import BeautifulSoup
import sqlite3
import os


def get_id_list(url, auctions=None):
    if auctions is None:
        auctions = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('span', {'class': 'text-blue3 pull-right copyMe wbc pl-2'})
    for r in results:
        auctions.append(r.text.strip())
    print(url)

    next_page = soup.find('li', {'class': 'next'}).find('a')

    if next_page:
        next_url = 'https://ubiz.ua' + next_page.get('href')
        get_id_list(next_url, auctions)

    return auctions


def get_auction_info(auction_id):
    main_url = 'https://ubiz.ua/sale3/auction/'

    response = requests.get(main_url + auction_id)
    soup = BeautifulSoup(response.text, 'lxml')

    cadnum = soup.find('p', {'data-atid': 'LandProps.cadastralNumber'}).text.strip()
    date = soup.find('span', {'data-atid': 'auctionPeriod.startDate'})
    area = soup.find('p', {'data-atid': 'LandProps.landArea'})

    country_element = soup.find('span', {'data-atid': 'items.address.countryName'})
    country = country_element.text.strip()
    region_element = soup.find('span', {'data-atid': 'items.address.region'})
    region = region_element.text.strip()
    locality_element = soup.find('span', {'data-atid': 'items.address.locality'})
    locality = locality_element.text.strip()
    address = f'{country}, {region}, {locality}'

    classification = soup.find('span', {'data-atid': 'items.classification.description'})

    return {
        'auction_id': auction_id,
        'cadnum': cadnum,
        'date': date.text.strip(),
        'area': area.text.strip(),
        'address': address,
        'classification': classification.text.strip()
    }


def add_to_database(auction):
    filename = 'auction.db'
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
            create table if not exists t_auction (
                id integer primary key autoincrement,
                auction_id text,
                cadnum text (22),
                date text,
                area text,
                address text,
                classification text
            )
        """
    cursor.execute(sql)

    cursor.execute('''insert into t_auction (auction_id, 
                                                   date,
                                                   cadnum,
                                                   area,
                                                   address,
                                                   classification
                                                   )
                            values (?, ?, ?, ?, ?, ?)''', (auction['auction_id'],
                                                           auction['date'],
                                                           auction['cadnum'],
                                                           auction['area'],
                                                           auction['address'],
                                                           auction['classification']))

    conn.commit()
    conn.close()


def get_existing_id(filename):
    ids = set()
    if not os.path.isfile(filename):
        return ids

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    sql = "SELECT auction_id FROM t_auction"
    rows = cursor.execute(sql).fetchall()

    for row in rows:
        ids.add(row[0])

    conn.close()
    return ids


if __name__ == '__main__':
    db_file = 'auction.db'
    regions_file = 'regions.txt'
    existing_id = get_existing_id(db_file)

    with open(regions_file, 'r') as f_regions:
        for region in f_regions:
            region = region.strip()
            id_list = get_id_list(f'https://ubiz.ua/auctions-all/land-rental/{region}/active-tendering')

            for list_element in id_list:
                if list_element not in existing_id:
                    data = get_auction_info(list_element)
                    add_to_database(data)
                    print("added new item: ", list_element)
