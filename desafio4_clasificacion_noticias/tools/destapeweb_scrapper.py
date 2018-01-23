# http://www.eldestapeweb.com/sitemap-news.xml
import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_destapeweb_article(html):
    article = {
        'section': '',
        'volanta': '',
        'headline': '',
        'bajada': '',
        'articleBody': ''
    }
    
    soup = BeautifulSoup(html, 'html.parser')
        
    header = soup.find('div', {'class': 'category-wrapper'})
    if header:
        # section
        section = header.find('a', {'class': 'category'})
        if section:          
            article['section'] = section.text.strip()
            
        # volanta
        volanta = header.find('a', {'class': 'category grouper'})
        if volanta:          
            article['volanta'] = volanta.text.strip()

    # headline
    headline = soup.find('h1', {'class': 'title'})
    if headline:
        article['headline'] = headline.text.strip()
        
    # bajada
    bajada = soup.find('p', {'class': 'preview'})
    if bajada:
        article['bajada'] = bajada.text.strip()
    
    # articleBody
    articleBody = soup.find('section', {'class': 'note-body'})
    if articleBody:
        article['articleBody'] = articleBody.text.strip()
    
    return article



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

links = []

xml_request = requests.get('http://www.eldestapeweb.com/sitemap-news.xml', headers)

print('grabbing El Destape Web links')
      
if xml_request.status_code == 200:
    soup = BeautifulSoup(xml_request.content, 'html.parser')
    urls = soup.find_all('url')
    for url in urls:
        loc = url.find('loc')
        links.append(loc.text)

print(len(links), 'obtained')
      
articles = []

for link in links:
    print('scrapping:', link)
    article_request = requests.get(link, headers)
    
    if article_request.status_code == 200:  
        article = parse_destapeweb_article(article_request.content)
        article['link'] = link
        article['source'] = 'eldestapeweb'
        articles.append(article)
        df = pd.DataFrame(articles)
        df.to_csv('eldestapeweb.csv', index=False)