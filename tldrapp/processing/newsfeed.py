import os
import feedparser
import requests
from BeautifulSoup import BeautifulSoup
from hashids import Hashids
from time import time


def get_feed_url(website):
    page = requests.get(website)
    soup = BeautifulSoup(page.text)
    link = soup.find('link', type='application/rss+xml')
    return link['href']


def get_news_items(feed_url):
    feed = feedparser.parse(feed_url)


current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_SAVE_PATH = os.path.join(current_dir, '../static/images/news/')
VALID_IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.gif')

image_url = ''
# Check that the image is valid
if image_url.lower().endswith(VALID_IMAGE_FORMATS):
    image_filename = os.path.split(image_url)[-1]
    image_filename = '{0}-{1}'.format(Hashids().encode(int(time())), image_filename)
    image_path = os.path.join(IMAGE_SAVE_PATH, image_filename)
    try:
        # Save the image
        pass
    except:
        image_path = ''
else:
    image_path = ''