from sqlalchemy import event
from hashids import Hashids
from .. import db
from .home import Summary
from pytldr.nlp.tokenizer import Tokenizer

# Will need to subclass the Summary model to include things like
# image, news source, original published date etc.
# Need to write a newsbot web crawler to populate tables with latest news
# from a selection of websites (BBC, Fox, CNN, Al Jazeera etc.)
# Crawler should be a cookie cutter, so that any given website can be
# crawled at a later date, perhaps even one provided by the user


class NewsSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    feed_url = db.Column(db.String(80))
    image_path = db.Column(db.String(80))

    def __init__(self, name, feed_url, image_path):
        self.name = name
        self.feed_url = feed_url
        self.image_path = image_path

    def __repr__(self):
        return '<NewsSource {0}>'.format(self.name)


class NewsSummary(Summary):
    title = db.Column(db.String)
    url = db.Column(db.String, unique=True)
    pub_date = db.Column(db.DateTime)
    image_path = db.Column(db.String(80))

    news_source_id = db.Column(db.Integer, db.ForeignKey('news_source.id'))
    news_source = db.relationship('NewsSource', backref=db.backref('summaries', lazy='dynamic'))

    def __init__(self,
                 title,
                 bullets,
                 highlighted_text,
                 news_source,
                 source_url,
                 date_added=None,
                 pub_date=None,
                 image_path='',
                 ):
        super(NewsSummary, self).__init__(
            bullets,
            highlighted_text,
            source_url=source_url,
            date_added=date_added)

        self.title = title
        self.news_source = news_source
        self.pub_date = pub_date
        self.image_path = image_path

    def __repr__(self):
        return '<NewsSummary {0}>'.format(self.title)


@event.listens_for(NewsSummary, "after_insert")
def update_url(mapper, connection, target):
    url_max_length = 30
    news_summary_table = mapper.local_table

    tokenizer = Tokenizer()
    title_clean = tokenizer.remove_all_punctuation(target.title.lower())
    title_clean = tokenizer.remove_stopwords(title_clean) if len(title_clean) > url_max_length else title_clean
    title_clean = title_clean[:url_max_length] if len(title_clean) > url_max_length else title_clean
    title_clean = title_clean.replace(' ', '-')

    url_hash = Hashids().encode(target.id)
    url = '{0}-{1}'.format(url_hash, title_clean)

    connection.execute(
          news_summary_table.update().
              values(url=url).
              where(news_summary_table.c.id==target.id)
    )