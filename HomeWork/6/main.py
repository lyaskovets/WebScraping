import requests
from bs4 import BeautifulSoup
import json


def parse_main_page(url, limit):
    main_page = url.replace('/sport', '')
    links = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    posts = soup.find_all('div', {'data-testid': 'promo', 'type': 'article'})

    for post in posts[:limit]:
        url_page = main_page + post.find('div').find('a').get('href').strip()
        links.append(url_page)

    return links


def get_topics(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    topics = soup.find('div', {'data-component': 'topic-list'}).find_all('li')
    result = [topic.find('a').text for topic in topics]

    return result


if __name__ == '__main__':

    links = parse_main_page('https://www.bbc.com/sport', 5)
    results = []
    for link in links:
        topics = get_topics(link)
        result = {"Link": link, "Topics": topics}
        results.append(result)
    with open('result.json', 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
