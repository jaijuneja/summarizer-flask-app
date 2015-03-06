from flask import Flask, render_template, request
from pytldr.summarize.textrank import TextRankSummarizer
from pytldr.summarize.lsa import LsaSummarizer
from pytldr.summarize.relevance import RelevanceSummarizer

app = Flask(__name__)
# app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    default_values = {
        'text': None,
        'algorithm': None,
        'length': 0.25,
    }
    summary_methods = [
        'TextRank',
        'Latent Semantic Analysis',
        'Relevance Score'
    ]
    summary = None

    if request.method == 'POST':
        form = dict()
        form['text'] = request.form['text'] if request.form['text'] else default_values['text']
        form['algorithm'] = request.form['algorithm'] if request.form['algorithm'] else default_values['algorithm']
        form['length'] = float(request.form['length']) if request.form['length'] else default_values['length']
        empty_fields = validate_input(form)
        if not empty_fields:
            summary, error = summarize(form['text'], form['algorithm'], form['length'])
        else:
            error = 'The following fields are missing: {0}'.format(
                ', '.join(empty_fields)
            )

    return render_template(
        'home.html',
        summary_methods=summary_methods,
        summary=summary,
        error=error,
    )


@app.route('/about/')
def about():
    return render_template('about.html')


def validate_input(form):
    return [field for field, val in form.items() if not val]


def summarize(text, algorithm, length):
    error = None
    if algorithm == 'Latent Semantic Analysis':
        summarizer = LsaSummarizer()
    elif algorithm == 'Relevance Score':
        summarizer = RelevanceSummarizer()
    elif algorithm == 'TextRank':
        summarizer = TextRankSummarizer()
    else:
        error = 'The summarization algorithm "{0}" does not exist'.format(algorithm)

    if not error:
        return (
            summarizer.summarize(text, length=length),
            None
        )
    else:
        return None, error


if __name__ == "__main__":
    app.run()
