import requests
import json
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'http://quotes.toscrape.com'
AUTHORS_FILE = 'authors.json'
QUOTES_FILE = 'quotes.json'


def get_soup(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except requests.RequestException as e:
        logger.error(f'Failed to fetch page {url}: {e}')
        return None


def get_authors_urls(soup: BeautifulSoup) -> list:
    urls = []
    try:
        about_links = soup.find_all('a', string='(about)')
        urls = [f"{BASE_URL}{link['href']}" for link in about_links]
    except AttributeError as e:
        logger.error(f'Error extracting author URLs: {e}')
    return urls


def get_authors(urls: list) -> list:
    authors = []
    for url in urls:
        soup = get_soup(url)
        if soup:
            author = {}
            try:
                author['fullname'] = soup.find('h3', class_='author-title').text
                author['born_date'] = soup.find('span', class_='author-born-date').text
                author['born_location'] = soup.find('span', class_='author-born-location').text
                author['description'] = soup.find('div', class_='author-description').text.strip()
                authors.append(author)
            except AttributeError as e:
                logger.error(f'Error extracting author details from {url}: {e}')
    return authors


def get_tags(soup: BeautifulSoup) -> list:
    tags_quotes = []
    try:
        quotes = soup.find_all('div', class_='quote')
        for q in quotes:
            tag_quote = {'author': q.find('small', itemprop='author').text, 'quote': q.find('span', class_='text').text}
            tags = q.find('meta', class_='keywords')
            if tags:
                tag_quote['tags'] = tags.get('content').split(',')
            tags_quotes.append(tag_quote)
    except AttributeError as e:
        logger.error(f'Error extracting quotes: {e}')
    return tags_quotes


def write_to_json(data: str, result: list):
    try:
        with open(data, 'w', encoding='utf-8') as fd:
            json.dump(result, fd, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f'Error writing to {data}: {e}')


def scrape_page(url: str):
    soup = get_soup(url)
    if soup:
        authors_urls = get_authors_urls(soup)
        authors = get_authors(authors_urls)
        write_to_json(AUTHORS_FILE, authors)

        tags_quotes = get_tags(soup)
        write_to_json(QUOTES_FILE, tags_quotes)


def scrape_all_pages(base_url: str):
    all_urls = [base_url]
    while True:
        soup = get_soup(all_urls[-1])
        if not soup:
            break
        next_page = soup.find('li', class_='next')
        if not next_page:
            break
        next_page_url = next_page.select_one('a')['href']
        next_url = f"{BASE_URL}{next_page_url}"
        all_urls.append(next_url)

    for url in all_urls:
        scrape_page(url)


def main():
    scrape_all_pages(BASE_URL)


if __name__ == '__main__':
    main()
