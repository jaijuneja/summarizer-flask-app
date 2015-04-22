# manage.py

from flask.ext.script import Manager

from .. import app
from ..processing.newsbot import NewsBot
from ..processing.newsrank import rank_news
from ..models.news import NewsSummary

manager = Manager(app)


@manager.option('-f', '--feed', dest='feed')
def update_news(feed):
    news_bot = NewsBot(
        feed,
        'TextRank',
        0.3
    )
    articles = news_bot.crawl(commit=True)


@manager.option('-i', '--inputarticles', dest='num_input_articles', default=500)
@manager.option('-o', '--outputarticles', dest='num_output_articles', default=0.5)
def rank_latest_news(num_input_articles, num_output_articles):
    articles = NewsSummary.query.order_by(NewsSummary.pub_date.desc()).limit(num_input_articles).all()
    article_titles = [article.title for article in articles]

    print num_input_articles, num_output_articles

    # Replace 'None' article titles with empty string
    for i, _ in enumerate(article_titles):
        article_titles[i] = '' if not article_titles[i] else article_titles[i]

    top_articles = rank_news(article_titles, length=num_output_articles)

    for ndx in top_articles:
        print article_titles[ndx]

if __name__ == "__main__":
    manager.run()