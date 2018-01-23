# scrap Clarin
from datetime import datetime, timedelta
import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import json
from bs4 import BeautifulSoup

def parse_clarin_html(html):
    article = {
        'section': '',
        'volanta': '',
        'headline': '',
        'bajada': '',
        'articleBody': ''
    }
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # section
    section = soup.find('div', {'class': 'title-box'})
    if section:
        article['section'] = section.text.strip()
    
    # volanta
    volanta = soup.find('p', {'class': 'volanta'})
    if volanta:
        article['volanta'] = volanta.text.strip()
        
    # headline
    headline = soup.find('h1', {'id': 'title'})
    if headline:
        article['headline'] = headline.text.strip()
    
    # bajada
    bajada = soup.find('div', {'class': 'bajada'})
    if bajada:
        article['bajada'] = bajada.text.strip()
    
    # articleBody
    articleBody = soup.find('div', {'class': 'body-nota'})
    if articleBody:
        article['articleBody'] = articleBody.text.strip()
    
    return article

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def get_links(date_yyyymmdd):
    links = []

    prev_links_url_base = 'https://www.clarin.com/ediciones-anteriores/archivo/pager.json?'
    for page in range(1,10):
        print('page', page)
        prev_links_url = prev_links_url_base + 'page=' + str(page) + '&date=' + date_yyyymmdd
        
        prev_links_request = requests.get(prev_links_url, headers)

        if prev_links_request.status_code != 200:
            return links

        response = json.loads(prev_links_request.content[1:-1])
        news = response['news']

        soup = BeautifulSoup(news, 'html.parser')
        scrapped_links = soup.find_all('a')
        for link in scrapped_links:
            href = link['href']
            if len(href) > 0:
                links.append('https://www.clarin.com' + href)

    return links
    
articles = []
days_delta = 1
while True:
    date = datetime.now() - timedelta(days=days_delta)
    date_yyyymmdd = date.strftime('%Y%m%d')
    print('getting link articles for', date_yyyymmdd)
    
    links = get_links(date_yyyymmdd)
    print('links obtained: ', len(links))
    
    for link in links:
        print('getting contents of article:', link)
        
        article_request = requests.get(link, headers)
        
        if article_request.status_code != 200:
            print('bad response!', article_request.content)
        else:
            article = parse_clarin_html(article_request.content)
            article['date'] = date
            article['link'] = link
            article['source'] = 'clarin'
            articles.append(article)
            
            df = pd.DataFrame(articles)
            df.to_csv('big_clarin_3.csv', index=False)
    
    days_delta = days_delta + 1
