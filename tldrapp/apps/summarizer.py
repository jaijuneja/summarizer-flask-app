from pytldr.summarize.textrank import TextRankSummarizer
from pytldr.summarize.lsa import LsaSummarizer
from pytldr.summarize.relevance import RelevanceSummarizer
from pytldr.nlp.preprocess import parse_input


def summarize(text, algorithm, length):
    summary = None
    error = None
    highlighted_text = None

    if algorithm == 'Latent Semantic Analysis':
        summarizer = LsaSummarizer()
    elif algorithm == 'Relevance Score':
        summarizer = RelevanceSummarizer()
    elif algorithm == 'TextRank':
        summarizer = TextRankSummarizer()
    else:
        error = 'The summarization algorithm "{0}" does not exist'.format(algorithm)

    if not error:
        summary = summarizer.summarize(text, length=length)
        original_text = parse_input(text)

        highlighted_text = get_highlighted_text(summary, original_text)

        if not summary:
            error = "The input text is too short to produce a summary. If you're submitting a link " \
                    "make sure that it starts with 'http://'."

    return summary, highlighted_text, error


def get_highlighted_text(summary, original_text):
        highlighted_text = list()
        cursor = 0
        # highlighted_text is [(text, bool_highlighted, paragraph_end), ...]
        for sentence in summary:
            text_pos = original_text[cursor:].find(sentence[:-3])
            text_pos += cursor
            if text_pos != -1:
                before = original_text[cursor:text_pos]
                if before:
                    paragraph = True if before.endswith('\n') else False
                    highlighted_text.append((before, False, paragraph))
                cursor = text_pos + len(sentence)
                highlighted_sentence = original_text[text_pos:cursor]
                paragraph = True if highlighted_sentence.endswith('\n') else False
                highlighted_text.append((highlighted_sentence, True, paragraph))

        end_text = original_text[cursor:]
        if end_text:
            paragraph = True if end_text.endswith('\n') else False
            highlighted_text.append((end_text, False, paragraph))
        
        return highlighted_text