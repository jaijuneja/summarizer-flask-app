from sqlalchemy import event
from hashids import Hashids
from datetime import datetime
from .. import db
from .custom_types import Json
from ..processing.summarizer import SummaryLoader


class Summary(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    bullets = db.Column(Json)
    highlighted_text = db.Column(Json)
    source_url = db.Column(db.String(80))
    date_added = db.Column(db.DateTime)
    url = db.Column(db.String(80), unique=True)

    class Meta:
        ordering = (('date_added', 'desc'),)

    def __init__(self,
                 bullets,
                 highlighted_text,
                 source_url='',
                 date_added=None):
        self.bullets = bullets
        self.highlighted_text = highlighted_text
        self.source_url = source_url
        if not date_added:
            date_added = datetime.utcnow()
        self.date_added = date_added

    def __repr__(self):
        return '<Summary {0}>'.format(self.url)

    def to_summarizer_object(self):
        return SummaryLoader(self.bullets, self.highlighted_text)


@event.listens_for(Summary, "after_insert")
def update_url_hash(mapper, connection, target):
    summary_table = mapper.local_table
    connection.execute(
          summary_table.update().
              values(url=Hashids().encode(target.id)).
              where(summary_table.c.id==target.id)
    )