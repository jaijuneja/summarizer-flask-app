from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from ..processing.summarizer import algorithms


class QuickipediaSearch(Form):
    search = StringField(
        'Search Wikipedia:',
        validators=[InputRequired()])

    algorithm = SelectField(
        'Summary algorithm:',
        validators=[InputRequired()],
        choices=zip(algorithms.names, algorithms.names))

