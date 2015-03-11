import wikipedia as wiki
import summarizer
from .. import settings
from requests import ConnectionError


def search(query):
    try:
        results = wiki.search(query)
        results = [(r, r.replace(' ', settings.QUICKIPEDIA_SPACE_PLACEHOLDER)) for r in results]
        return results, None
    except ConnectionError:
        error = 'Could not connect to Wikipedia.'
        return [], error


def url_to_summary(extension, algorithm):
    page_id = extension.replace(settings.QUICKIPEDIA_SPACE_PLACEHOLDER, ' ')
    page = wiki.page(page_id)
    title = page.title
    summary, highlighted_text, error = summarizer.summarize(page.content, algorithm, 0.2)
    return title, summary, highlighted_text, error