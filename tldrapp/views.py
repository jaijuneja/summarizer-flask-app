import re
import config
import forms
from apps import summarizer
from apps import quickipedia as qpedia
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    errors = []
    summary = None
    highlighted_text = None

    form = forms.SummarizerForm(request.form)

    if request.method == "POST" and form.validate():
        summary, error, highlighted_text = summarizer.summarize(
            form.text.data, form.algorithm.data, form.length.data
        )
        if error:
            errors.append(error)
    else:
        errors += forms.collect_errors(form)

    return render_template(
        'home.html',
        form=form,
        summary=summary,
        error=errors,
        highlighted_text=highlighted_text
    )


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/quickipedia', methods=['GET', 'POST'])
def quickipedia():
    errors = []
    results = None
    algorithm_ext = None

    form = forms.QuickipediaSearch(request.form)

    if request.method == 'POST' and form.validate():
        algorithm_ext = config.SUMMARY_METHODS_MAPPING.get(form.algorithm.data, '')
        results = qpedia.search(form.search.data)
        if not results:
            error = 'Your search returned no results.'
            errors.append(error)
    else:
        errors += forms.collect_errors(form)

    return render_template('quickipedia.html',
                           form=form,
                           algorithm=algorithm_ext,
                           results=results,
                           error=errors)


@app.route('/quickipedia/<wiki_page>/<algorithm>')
def quickipedia_results(wiki_page, algorithm):
    algorithm = config.SUMMARY_METHODS_MAPPING.get(algorithm, 'TextRank')
    title, (summary, error, highlighted_text) = qpedia.url_to_summary(wiki_page, algorithm)

    return render_template('quickipedia_summary.html',
                           error=error,
                           title=title,
                           summary=summary,
                           highlighted_text=highlighted_text)


@app.route('/news')
def news():
    return render_template('news.html')


def collect_input(form_values, default_values, *fields):
    output = dict()
    for field in fields:
        output[field] = form_values[field] if form_values[field] else default_values.get(field, '')

    return output