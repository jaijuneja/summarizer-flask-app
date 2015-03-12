import wikipedia
from requests import ConnectionError
from flask import Blueprint, render_template, request, flash, abort
from ..processing.summarizer import Summarizer, algorithms
from ..forms.quickipedia import QuickipediaSearch
from ..helpers import flash_errors

quickipedia = Blueprint('quickipedia', __name__)


@quickipedia.route('/', methods=['GET', 'POST'])
def index():
    results = None
    algorithm_url = None

    form = QuickipediaSearch(request.form)

    if request.method == 'POST' and form.validate():
        algorithm_url = algorithms.url_mapping.get(form.algorithm.data, '')
        results, error = search(form.search.data)
        if error:
            flash(error)
        if not results:
            flash('Your search returned no results.')

    flash_errors(form)

    return render_template('quickipedia/index.html',
                           form=form,
                           algorithm=algorithm_url,
                           results=results)


@quickipedia.route('/<wiki_page>/<algorithm>')
def results(wiki_page, algorithm):
    algorithm = algorithms.url_mapping.get(algorithm, '')
    try:
        title, summary = url_to_summary(wiki_page, algorithm)
        if summary.error:
            flash(summary.error)
        return render_template('quickipedia/summary.html',
                               title=title,
                               summary=summary)
    except wikipedia.exceptions.DisambiguationError:
        flash('Not a valid Wikipedia page. If you arrived here from the search feature, '
              'it may be because the page is a "Disambiguation" page (i.e. it just suggests other pages).')
        abort(404)


SPACE_PLACEHOLDER = '_'


def search(query):
    try:
        results = wikipedia.search(query)
        results = [(r, r.replace(' ', SPACE_PLACEHOLDER)) for r in results]
        return results, None
    except ConnectionError:
        error = 'Could not connect to Wikipedia.'
        return [], error


def url_to_summary(extension, algorithm):
    page_id = extension.replace(SPACE_PLACEHOLDER, ' ')
    page = wikipedia.page(page_id)
    title = page.title
    summary = Summarizer(page.content, algorithm, 0.2)
    return title, summary