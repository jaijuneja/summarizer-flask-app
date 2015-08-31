# manage.py

# To run in shell:
# python -m tldrapp.scheduled.manager update_news

import yaml
import os

from flask.ext.script import Manager

from .. import app
from ..processing.newsbot import NewsBot
from ..processing.newsrank import rank_news
from ..models.news import NewsSummary

manager = Manager(app)


@manager.option('-f', '--feed', dest='feed', default='feeds.yaml')
@manager.option('-c', '--category', dest='cat', default=None)
@manager.option('-s', '--site', dest='site', default=None)
def update_news(feed, cat, site):

    this_dir = os.path.dirname(__file__)
    feeds_path = os.path.join(this_dir, 'feeds.yaml')

    if feed.endswith('.yaml'):
        with open(feeds_path, 'r') as feeds_file:
            feeds = yaml.load(feeds_file)

            for xml_feed in feeds['feeds']:
                news_bot = NewsBot(
                    xml_feed['url'],
                    'TextRank',
                    0.3,
                    category=xml_feed.get('category', None),
                    site_name=xml_feed.get('name', None)
                )
                news_bot.crawl(commit=True)

    elif feed.endswith('.xml'):
        news_bot = NewsBot(
            feed,
            'TextRank',
            0.3,
            category=cat,
            site_name=site
        )
        news_bot.crawl(commit=True)

    else:
        print('Input --feed should be a path to a .yaml or .xml')


@manager.option('-i', '--inputarticles', dest='num_input_articles', default=500)
@manager.option('-o', '--outputarticles', dest='num_output_articles', default=0.5)
def rank_latest_news(num_input_articles, num_output_articles):
    articles = NewsSummary.query.order_by(NewsSummary.pub_date.desc()).limit(num_input_articles).all()
    article_titles = [article.title for article in articles]

    print len(articles)

    # Replace 'None' article titles with empty string
    for i, _ in enumerate(article_titles):
        article_titles[i] = '' if not article_titles[i] else article_titles[i]

    top_articles = rank_news(article_titles, length=num_output_articles)

    for ndx in top_articles:
        print article_titles[ndx]

if __name__ == "__main__":
    manager.run()