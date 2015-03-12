import os
from flask import Blueprint, render_template, request, flash, abort, url_for
from .. import db
from ..models.home import Summary
from ..forms.home import SummarizerForm
from ..processing.summarizer import Summarizer
from ..helpers import flash_errors

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
            url = form.text.data if form.text.data.startswith(('http://', 'https://')) else ''
            summary_db_entry = Summary(
                summary.summary,
                summary.highlighted_text,
                source_url=url)
            url_hash = summary_db_entry.get_sha()
            db.session.add(summary_db_entry)
            db.session.commit()

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
    db_entry = Summary.query.filter_by(sha=url_hash).first()
    if not db_entry:
        abort(404)

    summary = db_entry.to_summarizer_object()
    if summary.error:
        flash(summary.error)
        abort(404)

    source_url = db_entry.source_url

    return render_template(
        'home/summary.html',
        summary=summary,
        source_url=source_url
    )

@home.route('/about/')
def about():
    return render_template('home/about.html')