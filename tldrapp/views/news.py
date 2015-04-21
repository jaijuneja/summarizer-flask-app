from flask import g, Blueprint, render_template, request, redirect, url_for
from ..helpers import flash_errors
from ..models.news import NewsSummary
from ..forms.news import SearchForm
from .. import app
from config import MAX_SEARCH_RESULTS

news = Blueprint('news', __name__)

@app.before_request
def before_request():
    g.search_form = SearchForm()


@news.route('/')
@news.route('/page/<int:page>')
def index(page=1):
    # Need to store the typical query in a cache, some way of checking
    # modified date
    # Could also store sidebar stuff in the cache, similar articles etc.
    # For each article need a set of similar articles. These can be updated every day
    # for recent articles and a bit longer for older ones.
    # Flask-Cache with Redis is a good option
    results_per_page = app.config['NEWS_PER_PAGE']
    # results = NewsSummary.query.order_by(NewsSummary.pub_date.desc()).limit(10).all()
    results = NewsSummary.query.order_by(NewsSummary.pub_date.desc())\
        .paginate(page, results_per_page, False).items
    template = 'news/index.html' if page == 1 else 'news/news_items.html'
    return render_template(template, results=results, page=page)


@news.route('/<url_hash>')
def news_entry(url_hash):
    summary = NewsSummary.query.filter_by(url=url_hash).first_or_404()
    source_url = summary.source_url

    return render_template(
        'news/entry.html',
        summary=summary,
        source_url=source_url
    )


@news.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        return redirect(url_for('news.search_results', query=form.search.data))

    flash_errors(form)
    return render_template('news/search.html', form=form)


@news.route('/search/<query>')
def search_results(query):
    results = NewsSummary.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('news/search_results.html',
                           query=query,
                           results=results)