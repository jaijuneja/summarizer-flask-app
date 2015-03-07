import re
from flask import Flask, render_template, request
from pytldr.summarize.textrank import TextRankSummarizer
from pytldr.summarize.lsa import LsaSummarizer
from pytldr.summarize.relevance import RelevanceSummarizer
from pytldr.nlp.preprocess import parse_input


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
    highlighted_text = None

    if request.method == 'POST':
        form = dict()
        form['text'] = request.form['text'] if request.form['text'] else default_values['text']
        form['algorithm'] = request.form['algorithm'] if request.form['algorithm'] else default_values['algorithm']
        form['length'] = float(request.form['length']) if request.form['length'] else default_values['length']
        empty_fields = validate_input(form)
        if not empty_fields:
            summary, error, highlighted_text = summarize(form['text'], form['algorithm'], form['length'])
        else:
            error = 'The following fields are missing: {0}'.format(
                ', '.join(empty_fields)
            )

    return render_template(
        'home.html',
        summary_methods=summary_methods,
        summary=summary,
        error=error,
        highlighted_text=highlighted_text
    )


@app.route('/about/')
def about():
    return render_template('about.html')


def validate_input(form):
    # TODO: validate input types (e.g. length must be a number), return error message
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
        parsed_text = parse_input(text)
        summary = summarizer.summarize(text, length=length)

        formatted_text = list()
        cursor = 0
        for sentence in summary:
            text_pos = parsed_text.find(sentence[:-3])
            if text_pos != -1:
                before = parsed_text[cursor:text_pos]
                before_split = before.split('\n')
                before_split = [sen for sen in before_split if sen]
                for s in before_split[:-1]:
                    formatted_text.append((s, False, True))
                if before_split:
                    formatted_text.append((before_split[-1], False, False))
                cursor = text_pos + len(sentence)
                formatted_text.append((parsed_text[text_pos:cursor], True, False))

        return (
            summary,
            None,
            formatted_text
        )
    else:
        return None, error, None


if __name__ == "__main__":
    app.run()
