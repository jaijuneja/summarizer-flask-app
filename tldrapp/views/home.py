from flask import Blueprint, render_template, request, flash
from ..forms.home import SummarizerForm
from ..processing.summarizer import Summary
from ..helpers import flash_errors

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    summary = None

    form = SummarizerForm(request.form)

    if request.method == "POST" and form.validate():
        summary = Summary(form.text.data, form.algorithm.data, form.length.data)
        if summary.error:
            flash(summary.error)

    flash_errors(form)

    return render_template(
        'home/index.html',
        form=form,
        summary=summary,
    )


@home.route('/about/')
def about():
    return render_template('home/about.html')