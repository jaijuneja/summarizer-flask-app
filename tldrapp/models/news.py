import flask.ext.whooshalchemy as whooshalchemy

from whoosh.analysis import SimpleAnalyzer
from sqlalchemy import event
from hashids import Hashids
from pytldr.nlp.tokenizer import Tokenizer

from .home import Summary

from .. import app, db


class NewsSource(db.Model):
    __searchable__ = ['name']
    __analyzer__ = SimpleAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(32))
    feed_url = db.Column(db.String(80))
    image_path = db.Column(db.String(80))

    def __init__(self, name, image_path=''):
        self.name = name
        self.slug = Tokenizer().strip_all_punctuation(name.lower()).replace(' ', '_')
        if not image_path:
            self.image_path = '/static/images/news/sources/{0}.png'.format(self.slug)
        else:
            self.image_path = image_path

    def __repr__(self):
        return '<NewsSource {0}>'.format(self.name)


class NewsCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(32))

    def __init__(self, name):
        self.name = name

        tokenizer = Tokenizer()
        slug = tokenizer.strip_all_punctuation(name.lower())
        self.slug = slug.replace(' ', '_')

    def __repr__(self):
        return '<NewsCategory {0}>'.format(self.name)


class NewsSummary(Summary):
    __searchable__ = ['bullets']
    __analyzer__ = SimpleAnalyzer()

    __mapper_args__ = {'polymorphic_identity': 'newssummary',
                       'inherit_condition': (id == Summary.id)}

    title = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    image_path = db.Column(db.String(80))

    news_source_id = db.Column(db.Integer, db.ForeignKey('news_source.id'))
    news_source = db.relationship('NewsSource', backref=db.backref('summaries', lazy='dynamic'))

    news_category_id = db.Column(db.Integer, db.ForeignKey('news_category.id'))
    news_category = db.relationship('NewsCategory', backref=db.backref('summaries', lazy='dynamic'))

    def __init__(self,
                 title,
                 bullets,
                 highlighted_text,
                 news_source,
                 source_url,
                 news_category,
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
        self.news_category = news_category
        self.pub_date = pub_date
        if image_path:
            self.image_path = image_path
        else:
            self.image_path = news_source.image_path

    def __repr__(self):
        return '<NewsSummary {0}>'.format(self.title)


@event.listens_for(NewsSummary, "after_insert")
def update_url(mapper, connection, target):
    url_max_length = 30
    news_summary_table = mapper.local_table

    tokenizer = Tokenizer()
    title_clean = tokenizer.strip_all_punctuation(target.title.lower())
    title_clean = tokenizer.remove_stopwords(title_clean) if len(title_clean) > url_max_length else title_clean
    while len(title_clean) > url_max_length:
        title_clean = ' '.join(title_clean.split(' ')[:-1])  # Remove last word from title
    title_clean = title_clean.replace(' ', '-')

    url_hash = Hashids(min_length=4).encode(target.id)
    url = title_clean + '-' + url_hash

    connection.execute(
        news_summary_table.update().values(url=url).where(news_summary_table.c.id == target.id)
    )

# Add the summary table to the search index
whooshalchemy.whoosh_index(app, NewsSummary)
whooshalchemy.whoosh_index(app, NewsSource)