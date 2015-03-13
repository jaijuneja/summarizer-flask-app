from pytldr.summarize.textrank import TextRankSummarizer
from pytldr.summarize.lsa import LsaSummarizer
from pytldr.summarize.relevance import RelevanceSummarizer
from pytldr.nlp.preprocess import parse_input


class Algorithms:

    names = [
        'TextRank',
        'Latent Semantic Analysis',
        'Relevance Score'
    ]

    url_mapping = {
        'textrank': 'TextRank',
        'lsa': 'Latent Semantic Analysis',
        'relevance': 'Relevance Score',
        'TextRank': 'textrank',
        'Latent Semantic Analysis': 'lsa',
        'Relevance Score': 'relevance'
    }

algorithms = Algorithms()


class Summarizer(object):

    def __init__(self, text, algorithm, length):
        self.summary = None
        self.error = None
        self.highlighted_text = None

        text = parse_input(text)

        if algorithm == 'Latent Semantic Analysis':
            summarizer = LsaSummarizer()
        elif algorithm == 'Relevance Score':
            summarizer = RelevanceSummarizer()
        elif algorithm == 'TextRank':
            summarizer = TextRankSummarizer()
        else:
            self.error = 'The summarization algorithm "{0}" does not exist'.format(algorithm)

        if not self.error:
            self.summary = summarizer.summarize(text, length=length)

            self.highlighted_text = self.get_highlighted_text(text)

            if not self.summary:
                self.error = "The input text is too short to produce a summary. If you're submitting a link " \
                             "make sure that it starts with 'http://'. Otherwise, we recommend you copy and paste " \
                             "the text directly below."

    def get_highlighted_text(self, text):
            highlighted_text = list()
            cursor = 0
            # highlighted_text is [(text, bool_highlighted, paragraph_end), ...]
            for sentence in self.summary:
                text_pos = text[cursor:].find(sentence[:-3])
                text_pos += cursor
                if text_pos != -1:
                    before = text[cursor:text_pos]
                    if before:
                        paragraph = True if before.endswith('\n') else False
                        highlighted_text.append((before, False, paragraph))
                    cursor = text_pos + len(sentence)
                    highlighted_sentence = text[text_pos:cursor]
                    paragraph = True if highlighted_sentence.endswith('\n') else False
                    highlighted_text.append((highlighted_sentence, True, paragraph))

            end_text = text[cursor:]
            if end_text:
                paragraph = True if end_text.endswith('\n') else False
                highlighted_text.append((end_text, False, paragraph))

            return highlighted_text


class SummaryLoader(object):

    def __init__(self, summary, highlighted_text):
        self.error = None
        if not (isinstance(summary, list) or isinstance(highlighted_text, list)) or not (summary or highlighted_text):
            self.error = 'The summary failed to load'

        self.summary = summary
        self.highlighted_text = highlighted_text