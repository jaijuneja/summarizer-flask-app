import config
from flask_wtf import Form
from flask_wtf.html5 import URLField
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import NumberRange, InputRequired, URL
from wtforms.widgets import TextArea


class SummarizerForm(Form):
    text = StringField(
        'Text or URL to summarize:',
        validators=[InputRequired()],
        widget=TextArea())

    algorithm = SelectField(
        'Algorithm:',
        validators=[InputRequired()],
        choices=zip(config.SUMMARY_METHODS, config.SUMMARY_METHODS))

    length = FloatField(
        'Length (# of sentences or % of original text):',
        validators=[NumberRange(min=0)],
        default=0.2)


class QuickipediaSearch(Form):
    search = StringField(
        'Search Wikipedia:',
        validators=[InputRequired()])

    algorithm = SelectField(
        'Summary algorithm:',
        validators=[InputRequired()],
        choices=zip(config.SUMMARY_METHODS, config.SUMMARY_METHODS))


def collect_errors(form):
    error_list = []
    for field, errors in form.errors.iteritems():
        messages = ['{0}: {1}'.format(field, error) for error in errors]
        error_list += messages

    return error_list