from flask import g, Blueprint, render_template, request, redirect, url_for, flash
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
def index():
    return render_template('news/index.html')


@news.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        return redirect(url_for('news.search_results', query=form.search.data))

    flash_errors(form)
    return render_template('news/search.html', form=form)
    # if not g.search_form.validate_on_submit():
    #     flash("You must enter a search term")
    #     return redirect(url_for('news.search'))
    # return redirect(url_for('news.search_results', query=g.search_form.search.data))


@news.route('/search/<query>')
def search_results(query):
    results = NewsSummary.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('news/search_results.html',
                           query=query,
                           results=results)