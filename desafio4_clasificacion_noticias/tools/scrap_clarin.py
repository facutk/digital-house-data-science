import requests
import json
from time import sleep
import pandas as pd
save_folder = './clarin/'

def process_line(s):
    print('waiting 10 seconds before requesting data...')
    sleep(10)
    print('wait done!')
    
    print('requesting:', s['url'])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    clarin_request = requests.get(s['url'], headers)
    
    if clarin_request.status_code == 200:
        print('request success!')
        print('saving file as:', save_folder + s['id'] + '.html')
        with open(save_folder + s['id'] + '.html', 'w') as file:
            file.write(clarin_request.text)
    else:
        print('request failed with status:', clarin_request.status_code)

    s['status'] = clarin_request.status_code
    return s

if __name__ == "__main__":
    df = pd.read_csv('./reddit_clarin_links.csv')
    df = df.apply(process_line, axis=1)
    df.to_csv('./reddit_clarin_links_processed.csv', index=False)
