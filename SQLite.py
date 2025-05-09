import sqlite3
import requests

# Set up DB
conn = sqlite3.connect('hacker_news.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT,
        score INTEGER,
        time INTEGER
    )
''')
conn.commit()

# Fetch stories
TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

story_ids = requests.get(TOP_STORIES_URL).json()[:5]

for sid in story_ids:
    story = requests.get(ITEM_URL.format(sid)).json()
    c.execute('''
        INSERT OR IGNORE INTO stories (id, title, url, score, time)
        VALUES (?, ?, ?, ?, ?)
    ''', (story['id'], story['title'], story.get('url'), story.get('score', 0), story['time']))
    conn.commit()

# Show results
c.execute('SELECT title, score FROM stories ORDER BY score DESC')
for title, score in c.fetchall():
    print(f"{title} - {score} points")

conn.close()
