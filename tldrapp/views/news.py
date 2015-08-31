from flask import g, Blueprint, render_template, request, redirect, url_for, abort
from ..helpers import flash_errors
from ..models.news import NewsSummary, NewsCategory, NewsSource
from ..forms.news import SearchForm
from ..cache import cache
from .. import app
from ..processing.newsrank import rank_news
from config import MAX_SEARCH_RESULTS

news = Blueprint('news', __name__)

@app.before_request
def before_request():
    g.search_form = SearchForm()


@cache.memoize()
@news.route('/')
@news.route('/page/<int:page>')
def index(page=1):
    results_per_page = app.config['NEWS_PER_PAGE']
    results = NewsSummary.query\
        .order_by(NewsSummary.pub_date.desc())\
        .paginate(page, results_per_page, False).items

    sidebar = get_hot_sidebar('', '')
    categories, sources = get_bottom_nav()

    template = 'news/index.html' if page == 1 else 'news/news_items.html'
    return render_template(template, results=results, sidebar=sidebar, page=page, categories=categories, sources=sources)


@cache.memoize()
@news.route('/category/<category>/')
@news.route('/category/<category>/page/<int:page>')
def category_page(category, page=1):
    results_per_page = app.config['NEWS_PER_PAGE']
    results = NewsSummary.query.join(NewsCategory)\
        .filter(NewsCategory.slug == category)\
        .order_by(NewsSummary.pub_date.desc())\
        .paginate(page, results_per_page, False).items

    if not results:
        abort(404)

    sidebar = get_hot_sidebar('category', category)
    categories, sources = get_bottom_nav()

    template = 'news/index.html' if page == 1 else 'news/news_items.html'
    return render_template(template, results=results, sidebar=sidebar, page=page, categories=categories, sources=sources)


@cache.memoize()
@news.route('/source/<source>/')
@news.route('/source/<source>/page/<int:page>')
def source_page(source, page=1):
    results_per_page = app.config['NEWS_PER_PAGE']
    results = NewsSummary.query.join(NewsSource)\
        .filter(NewsSource.slug == source)\
        .order_by(NewsSummary.pub_date.desc())\
        .paginate(page, results_per_page, False).items

    if not results:
        abort(404)

    sidebar = get_hot_sidebar('source', source)
    categories, sources = get_bottom_nav()

    template = 'news/index.html' if page == 1 else 'news/news_items.html'
    return render_template(template, results=results, sidebar=sidebar, page=page, categories=categories, sources=sources)


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


@cache.memoize()
def get_hot_sidebar(category_type, category_name, num_input_articles=500, num_output_articles=10):
    if category_type == 'category':
        articles = NewsSummary.query.join(NewsCategory)\
            .filter(NewsCategory.slug == category_name)\
            .order_by(NewsSummary.pub_date.desc()).limit(num_input_articles).all()
    elif category_type == 'source':
        articles = NewsSummary.query.join(NewsSource)\
            .filter(NewsSource.slug == category_name)\
            .order_by(NewsSummary.pub_date.desc()).limit(num_input_articles).all()
    else:
        articles = NewsSummary.query.order_by(NewsSummary.pub_date.desc()).limit(num_input_articles).all()

    article_titles = [article.title for article in articles]

    # Replace 'None' article titles with empty string
    for i, _ in enumerate(article_titles):
        article_titles[i] = '' if not article_titles[i] else article_titles[i]

    top_articles = rank_news(article_titles, length=num_output_articles)

    return [articles[i] for i in top_articles]


@cache.memoize()
def get_bottom_nav():
    categories = NewsCategory.query.order_by(NewsCategory.name.asc()).all()
    sources = NewsSource.query.order_by(NewsSource.name.asc()).all()
    return categories, sources