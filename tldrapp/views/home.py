import os

from flask import Blueprint, render_template, request, flash, url_for

from .. import db
from ..models.home import Summary
from ..forms.home import SummarizerForm
from ..processing.summarizer import Summarizer
from ..helpers import flash_errors
from ..processing.newsbot import NewsBot

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    url = ''

    form = SummarizerForm(request.form)

    if request.method == "POST" and form.validate():
        summary = Summarizer(form.text.data, form.algorithm.data, form.length.data)
        if summary.error:
            flash(summary.error)
        else:
            source_url = form.text.data if form.text.data.startswith(('http://', 'https://')) else ''
            summary_db_entry = Summary(
                summary.bullets,
                summary.highlighted_text,
                source_url=source_url)
            db.session.add(summary_db_entry)
            db.session.commit()

            url_hash = summary_db_entry.url
            url = os.path.join(request.url, url_for('home.summary_entry', url_hash=url_hash)[1:])

    flash_errors(form)

    return render_template(
        'home/index.html',
        form=form,
        summary=summary,
        url=url
    )


@home.route('/s/<url_hash>')
def summary_entry(url_hash):
    summary = Summary.query.filter_by(url=url_hash).first_or_404()
    source_url = summary.source_url

    return render_template(
        'home/summary.html',
        summary=summary,
        source_url=source_url
    )

@home.route('/about')
@home.route('/about/')
def about():
    return render_template('home/about.html')


@home.route('/news_bot')
def news_bot():
    news_bot = NewsBot(
        'http://feeds.bbci.co.uk/news/world/rss.xml',
        'TextRank',
        0.3
    )
    articles = news_bot.crawl(commit=True)
    return