import feedparser
import requests
from BeautifulSoup import BeautifulSoup


def get_feed_url(website):
    page = requests.get(website)
    soup = BeautifulSoup(page.text)
    link = soup.find('link', type='application/rss+xml')
    return link['href']


def get_news_items(feed_url):
    feed = feedparser.parse(feed_url)


