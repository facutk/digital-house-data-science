import requests
from bs4 import BeautifulSoup

def parse_token(content):
    soup = BeautifulSoup(content, 'lxml')
    return soup.find('input', {'name':'_csrf'})['value']
    
def parse_bpm(content):
    soup = BeautifulSoup(content, 'lxml')
    first_card = soup.find('div', { 'class' : 'card' })
    if not first_card:
        return None
    media_right = first_card.find('div', { 'class' : 'media-right' })
    titles = media_right.findAll('p', { 'class' : 'title' })
    return int(titles[1].text)

def scrap_bpm(artist = '', song = ''):
    with requests.Session() as s:
        r1 = s.get('https://songbpm.com')
        token = parse_token(r1.text)
        r2 = s.post('https://songbpm.com/searches', data = {'_csrf': token, 'q': '%s %s'%(artist, song)})
        return parse_bpm(r2.text)

import pandas as pd
df = pd.read_csv('../Data/billboard.csv', encoding='latin1')

import time

def process(df):
    time.sleep(3)
    bpm = scrap_bpm(df['artist.inverted'], df['track'])
    df['bpm'] = bpm
    print('%s, %s, %s'%(df['artist.inverted'], df['track'], str(bpm)))
    return df

artist_track = df[['artist.inverted', 'track']]
artist_track = artist_track.apply(process, axis = 1)


artist_track.to_csv('./bpm_scrapped.csv', encoding='latin1', index = False)
