import pandas as pd 
import re 
import requests
from bs4 import BeautifulSoup
import time
import random

#Only if you start from the list 

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]

def load_existing_data(file_path):
    try:
        existing_data = pd.read_csv(file_path)
        data = existing_data.to_dict(orient='records')
        print(f'Resuming from link {len(data)}.')
        return data
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print('Starting from scratch.')
        return []

def read_links_from_file():
    with open('anime_links.txt', 'r') as f:
        return f.read().splitlines()

def get_last_episode_number(scripts):
    for script in scripts:
        if script.string:
            episodes_search = re.search(r'var episodes = \[\[(\d+),\d+\]', script.string)
            if episodes_search:
                return episodes_search.group(1)
    return None

def get_anime_data(soup):
    title = soup.find('h1', class_='Title').text
    tv_type = soup.find('h1').find_next_sibling('span').text
    alt_title_1 = soup.find('span', class_='TxtAlt')
    alt_title_1_text = alt_title_1.text.strip() if alt_title_1 else None
    alt_title_2 = alt_title_1.find_next_sibling('span', class_='TxtAlt') if alt_title_1 else None
    alt_title_2_text = alt_title_2.text.strip() if alt_title_2 else None
    rating = soup.find('span', class_='vtprmd')
    rating = rating.text if rating else None
    description = soup.find('div', class_='Description').text.replace('\n', '')
    genres = [a.text for a in soup.find('nav', class_='Nvgnrs').find_all('a')]
    followers = soup.find('div', class_='Top').find('div', class_='Title').text.replace('Seguidores: ', '')
    status = soup.find('span', class_='fa-tv').text
    return {
        'title': title,
        'type_tv': tv_type,
        'alt_title_1': alt_title_1_text,
        'alt_title_2': alt_title_2_text,
        'rating': rating,
        'description': description,
        'genres': genres,
        'followers': followers,
        'status': status
    }

def process_link(link):
    headers = {'User-Agent': random.choice(user_agents)}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    scripts = soup.find_all('script')
    last_episode_number = get_last_episode_number(scripts)
    anime_data = get_anime_data(soup)
    anime_data['url'] = link
    anime_data['last_episode_number'] = last_episode_number
    return anime_data

def save_data(data):
    pd.DataFrame(data).to_csv('anime_data.csv', index=False)

def scraper():
    data = []
    check_point = 50
    links = read_links_from_file()
    for i, link in enumerate(links, 1):
        try:
            data.append(process_link(link))
        except Exception as e:
            print(f'Failed to process {link}: {type(e).__name__}, {e}')
        if i % check_point == 0:
            save_data(data)
            print(f'Saved checkpoint at link {i}.')
        time.sleep(random.randint(1, 5))
    if i % check_point != 0:
        save_data(data)
    return data

def main():
    data = load_existing_data('anime_data.csv')
    data.extend(scraper())
    pd.DataFrame(data).to_csv('anime_data.csv', index=False)
    print(f'Scraped {len(data)} links')

if __name__ == "__main__":
    main()

