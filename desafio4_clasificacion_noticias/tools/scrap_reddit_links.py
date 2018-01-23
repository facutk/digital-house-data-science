import requests
import json
from time import sleep

def gen_reddit_json_link(link_id):
    return 'https://www.reddit.com/domain/clarin.com/new.json?after=t3_' + link_id

def save_reddit_json(post_id, parsed_json):
    with open('./reddit/' + post_id + '.json', 'w') as f:
        json.dump(parsed_json, f)

def get_next_post_id(parsed_json):
    children = parsed_json['data']['children']
    next_post_id = children[len(children) - 1]['data']['id']
    return next_post_id

def scrap_reddit(post_id = '6z8i1d', wait_multiplier = 1):
    print('scrapping:', post_id)
    print('waiting 3 min before requesting data...')
    sleep(3 * 60)
    print('wait done!')
    
    reddit_json_link = gen_reddit_json_link(post_id)
    
    print('requesting:', reddit_json_link)
    reddit_json_request = requests.get(reddit_json_link, headers = {'User-agent': 'Clarin links 1.0'})
    
    if reddit_json_request.status_code == 200:
        print('request success!')
        print('parsing content')
        reddit_json_response = reddit_json_request.content
        parsed_json = json.loads(reddit_json_response)
        
        print('saving:', post_id)
        save_reddit_json(post_id, parsed_json)
        
        next_post_id = get_next_post_id(parsed_json)
        scrap_reddit(next_post_id)
    else:
        print('request failed with status:', reddit_json_request.status_code)
        print(reddit_json_request.content)
        print('sleeping for', 5 * wait_multiplier, 'minutes...')
        sleep(5 * 60 * wait_multiplier)
        scrap_reddit(post_id, wait_multiplier + 1)

if __name__ == "__main__":
    scrap_reddit()
