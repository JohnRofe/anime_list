import requests
from bs4 import BeautifulSoup
import time
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]


BASE_URL = "https://www3.animeflv.net/browse?page="  
ANIME_URL = "https://www3.animeflv.net"

def get_anime_links(page):
    url = BASE_URL + str(page)
    headers = {'User-Agent': random.choice(user_agents)}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    anime_links = soup.find_all('article', class_='Anime alt B') 
    return [ANIME_URL + anime.find('a')['href'] for anime in anime_links]


def scrape_anime_links():
    page = 1
    failures = 0 
    links = []

    while True:
        try:
            new_links = get_anime_links(page)
            if not new_links:
                failures += 1
            else:
                failures = 0
                links.extend(new_links)
            page += 1
        except Exception:
            failures += 1

        if failures >= 2:
            break

        time.sleep(random.randint(5, 10))

    return list(set(links))  # remove duplicates
    
def save_links_to_file(links):
    with open('anime_links.txt', 'a') as f:
        for link in links:
            f.write(link + "\n")

def main():
    links = scrape_anime_links()
    save_links_to_file(links)
    print(f"Scraped {len(links)} links")

if __name__ == "__main__":
    main()