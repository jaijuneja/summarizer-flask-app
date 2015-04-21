# manage.py

from flask.ext.script import Manager

from .. import app
from ..processing.newsbot import NewsBot

manager = Manager(app)


@manager.option('-f', '--feed', dest='feed')
def update_news(feed):
    news_bot = NewsBot(
        feed,
        'TextRank',
        0.3
    )
    articles = news_bot.crawl(commit=True)

if __name__ == "__main__":
    manager.run()