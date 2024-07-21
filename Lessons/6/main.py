import requests
from bs4 import BeautifulSoup
import re
import hashlib
import os
import json


def parse_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
           <library>
               <book>
                   <title>To Kill a Mockingbird</title>
                   <author>Harper Lee</author>
                   <year>1960</year>
                   <isbn>978-0-06-112008-4</isbn>
               </book>
               <book>
                   <title>1984</title>
                   <author>George Orwell</author>
                   <year>1949</year>
                   <isbn>978-0-452-28423-4</isbn>
               </book>
               <book>
                   <title>The Great Gatsby</title>
                   <author>F. Scott Fitzgerald</author>
                   <year>1925</year>
                   <isbn>978-0-7432-7356-5</isbn>
               </book>
           </library>
       """
    soup = BeautifulSoup(xml, features='xml')
    book = soup.find('book')
    # print(book)

    g = soup.find(string='The Great Gatsby')
    # print(g)

    titles_regexp = soup.find_all('title', string=re.compile('Kill|Gatsby'))
    print(titles_regexp)

    titles = soup.find_all('title')

    titles = [t.text for t in titles]
    years = [t.text for t in soup.find_all('year')]
    for t, y in zip(titles, years):
        print(f'book "{t}" was witten {y}')


def get_content(url):
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        return content

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    with open(filename, 'w') as f:
        f.write(response.text)
    return response.text


def parse_html():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [b.parent for b in blocks if b.get('class') is None]

    for b in blocks:
        title = b.find('h3').text.strip()
        url = b.find('h3').find('a').get('href').strip()
        salary_tag = b.find('p', {'class': 'salary-city__vacancy'})
        salary_value = salary_tag.text.strip() if salary_tag else ''
        data.append({'title': title, 'url': url, 'salary': salary_value})

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_page(page_url):
    content = get_content(page_url)
    soup = BeautifulSoup(content, 'lxml')
    site = soup.find('dt', string='Сайт:').find_next_sibling('dd').find('a').text.strip()
    return {'url': page_url, 'site': site}


def parse_sync():
    url = 'https://job.morion.ua/jobs/'
    content = get_content(url)

    soup = BeautifulSoup(content, 'lxml')

    data = []

    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]

    for block in blocks:
        url = block.find('h3').find('a').get('href').strip()
        page_data = parse_page(url)
        data.append(page_data)

    with open('sync.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    # parse_xml()
    # parse_html()
    # print(parse_page('https://job.morion.ua/vacancy/13894932892/'))
    parse_sync()