from flask_wtf import Form
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import NumberRange, InputRequired
from wtforms.widgets import TextArea
from ..processing.summarizer import algorithms


class SummarizerForm(Form):
    text = StringField(
        'Text or URL to summarize:',
        validators=[InputRequired()],
        widget=TextArea())

    algorithm = SelectField(
        'Algorithm:',
        validators=[InputRequired()],
        choices=zip(algorithms.names, algorithms.names))

    length = FloatField(
        'Length (# of sentences or % of original text):',
        validators=[NumberRange(min=0)],
        default=0.2)
