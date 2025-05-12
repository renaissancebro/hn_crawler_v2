import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
from datetime import datetime
from typing import Optional
from watchdog import run_with_watchdog

TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

def crawl_hn():
    response = requests.get(TOP_STORIES_URL)
    top_story_ids = response.json()[:10]  # Limit for demo

    stories: list[dict[str, Optional[str]]] = [] #type hint for list of dictionaries containing string values

    for idx, sid in enumerate(top_story_ids):
        #print(f"Fetching story {idx + 1}/{len(top_story_ids)} (ID: {sid})")
        msg: str = f"Fetching stroy {idx+1}/{len(top_story_ids)}(ID: {sid})"
        print(msg)
        logging.info(msg)
        story = requests.get(ITEM_URL.format(sid)).json()
        if story is None:
            continue

        title = story.get('title', 'N/A')
        url = story.get('url', None)
        ext_title = 'N/A'

        if url:
            try:
                page = requests.get(url, timeout=5)
                soup = BeautifulSoup(page.text, 'html.parser')
                ext_title_tag = soup.find('title')
                if ext_title_tag:
                    ext_title = ext_title_tag.get_text(strip=True)
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                logging.warning(f"Failed to fetch {url}: {e}")

        stories.append({
            'hn_title': title,
            'hn_url': url,
            'external_title': ext_title
        })

        time.sleep(0.5)  # Be nice to servers

    # Timestamped filename
    filename = f"hn_crawled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['hn_title', 'hn_url', 'external_title'])
        writer.writeheader()
        for story in stories:
            writer.writerow(story)

    print(f"Saved {len(stories)} stories to {filename}")
    logging.info(f"Saved {len(stories)} stories to {filename}")

if __name__ == "__main__":
    run_with_watchdog(crawl_hn)
