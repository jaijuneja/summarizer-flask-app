import settings
import forms
import wikipedia
import utils
from apps import summarizer
from apps import quickipedia as qpedia
from flask import Flask, render_template, request, flash

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    highlighted_text = None

    form = forms.SummarizerForm(request.form)

    if request.method == "POST" and form.validate():
        summary, highlighted_text, error = summarizer.summarize(
            form.text.data, form.algorithm.data, form.length.data
        )
        if error:
            flash(error)

    utils.flash_errors(form)

    return render_template(
        'home.html',
        form=form,
        summary=summary,
        highlighted_text=highlighted_text
    )


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/quickipedia', methods=['GET', 'POST'])
def quickipedia():
    results = None
    algorithm_ext = None

    form = forms.QuickipediaSearch(request.form)

    if request.method == 'POST' and form.validate():
        algorithm_ext = settings.SUMMARY_METHODS_MAPPING.get(form.algorithm.data, '')
        results, error = qpedia.search(form.search.data)
        if error:
            flash(error)
        if not results:
            flash('Your search returned no results.')

    utils.flash_errors(form)

    return render_template('quickipedia/quickipedia.html',
                           form=form,
                           algorithm=algorithm_ext,
                           results=results)


@app.route('/quickipedia/<wiki_page>/<algorithm>')
def quickipedia_results(wiki_page, algorithm):
    algorithm = settings.SUMMARY_METHODS_MAPPING.get(algorithm, 'TextRank')
    try:
        title, summary, highlighted_text, error = qpedia.url_to_summary(wiki_page, algorithm)
        if error:
            flash(error)
        return render_template('quickipedia/quickipedia_summary.html',
                               title=title,
                               summary=summary,
                               highlighted_text=highlighted_text)
    except wikipedia.exceptions.DisambiguationError:
        flash('Not a valid Wikipedia page. If you arrived here from the search feature, '
              'it may be because the page is a "Disambiguation" page (i.e. it just suggests other pages).')
        return render_template('404.html')

@app.route('/news')
def news():
    return render_template('news/news.html')