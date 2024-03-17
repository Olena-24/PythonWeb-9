import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'
AUTHORS_FILE = 'authors.json'
QUOTES_FILE = 'quotes.json'

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_author_details(author_url):
    soup = get_soup(author_url)
    author = {}
    author['fullname'] = soup.find('h3', class_='author-title').text
    author['born_date'] = soup.find('span', class_='author-born-date').text
    author['born_location'] = soup.find('span', class_='author-born-location').text
    author['description'] = soup.find('div', class_='author-description').text.strip()
    return author

def get_tags(soup):
    quotes = soup.find_all('div', class_='quote')
    tags_quotes = []
    for q in quotes:
        tag_quote = {'author': q.find('small', itemprop='author').text, 'quote': q.find('span', class_='text').text}
        tags = q.find('meta', class_='keywords')
        if tags:
            tag_quote['tags'] = tags.get('content').split(',')
        tags_quotes.append(tag_quote)
    return tags_quotes

def write_to_json(data, result):
    with open(data, 'w', encoding='utf-8') as fd:
        json.dump(result, fd, ensure_ascii=False, indent=2)

def scrape_quotes():
    all_quotes = []
    page_url = BASE_URL
    while page_url:
        soup = get_soup(page_url)
        all_quotes.extend(get_tags(soup))
        next_page = soup.find('li', class_='next')
        page_url = BASE_URL + next_page.a['href'] if next_page else None
    return all_quotes

def scrape_authors():
    author_urls = [BASE_URL + link['href'] for link in get_soup(BASE_URL).find_all('a', text='(about)')]
    authors = [get_author_details(url) for url in author_urls]
    return authors

def main():
    authors = scrape_authors()
    quotes = scrape_quotes()
    write_to_json(AUTHORS_FILE, authors)
    write_to_json(QUOTES_FILE, quotes)

if __name__ == '__main__':
    main()